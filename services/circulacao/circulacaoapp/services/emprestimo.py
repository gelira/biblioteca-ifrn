import os
from django.utils import timezone
from django.db import transaction
from rest_framework.exceptions import APIException

from .. import exceptions
from ..models import Emprestimo, Reserva, Renovacao

from .base import (
    send_task_group,
    datetime_name, 
    save_clocked_task,
    save_batch_clocked_tasks,
    try_to_send
)
from .autenticacao import AutenticacaoService
from .notificacao import NotificacaoService
from .catalogo import CatalogoService
from .reserva import ReservaService
from .feriado import FeriadoService

CIRCULACAO_QUEUE = os.getenv('CIRCULACAO_QUEUE')

class EmprestimoService:
    task_emprestimo_avaliado = 'circulacao.emprestimo_avaliado'
    task_enviar_comprovante_emprestimo = 'circulacao.enviar_comprovante_emprestimo'
    task_agendar_alertas_emprestimo = 'circulacao.agendar_alertas_emprestimo'
    task_enviar_comprovante_renovacao = 'circulacao.enviar_comprovante_renovacao'
    task_checar_emprestimo = 'circulacao.checar_emprestimo'

    @classmethod
    def check_livro_emprestado_usuario(cls, usuario_id, livro_id):
        if Emprestimo.objects.filter(
            usuario_id=usuario_id,
            livro_id=livro_id,
            data_devolucao=None
        ).exists():
            raise exceptions.LivroEmprestadoUsuario

    @classmethod
    def check_emprestimos_usuario(cls, usuario_id, max_livros, quantidade_livros):
        emprestimos_vigentes = Emprestimo.objects.filter(
            usuario_id=usuario_id,
            data_devolucao=None
        )

        livros_emprestados_id = list(map(lambda x: str(x.livro_id), emprestimos_vigentes))

        if (len(livros_emprestados_id) + quantidade_livros) > max_livros:
            raise exceptions.LimiteEmprestimos

        return livros_emprestados_id

    @classmethod
    def check_codigos(cls, usuario_id, codigos, livros_emprestados_id):
        hoje = timezone.localdate()

        emprestar_referencia = FeriadoService.check_emprestimo_exemplar_referencia()
        exemplares = []
        reservas = {}

        for codigo in codigos:
            exemplar = CatalogoService.consulta_codigo_exemplar(codigo)

            if not exemplar['ativo']:
                raise APIException('Exemplar {} inativo'.format(codigo))

            if not exemplar['disponivel']:
                raise APIException('Exemplar {} indisponível'.format(codigo))

            if exemplar['referencia'] and not emprestar_referencia:
                raise APIException('Exemplar {} referência, não pode ser emprestado hoje'.format(codigo))

            livro_id = exemplar['livro']['_id']

            if livro_id in livros_emprestados_id:
                raise exceptions.ExemplarLivroEmprestadoUsuario

            reserva = ReservaService.base_queryset(
                hoje=hoje, 
                usuario_id=usuario_id, 
                livro_id=livro_id
            ).first()

            if reserva is not None:
                reservas[livro_id] = reserva
            else:
                exemplares_disponiveis = exemplar['livro']['exemplares_disponiveis']
                qtd_reservas = ReservaService.base_queryset(hoje=hoje, livro_id=livro_id).count()
                
                if exemplares_disponiveis <= qtd_reservas:
                    raise APIException('Existem reservas para o exemplar {}'.format(codigo))
            
            livros_emprestados_id.append(livro_id)
            exemplares.append(exemplar)

        return exemplares, reservas

    @classmethod
    def create_emprestimos(cls, exemplares, codigos, reservas, usuario, atendente_id):
        data_limite = FeriadoService.calcular_data_limite(usuario['perfil']['max_dias'])
        data_limite_referencia = FeriadoService.calcular_data_limite()
        
        usuario_id = usuario['_id']

        emprestimos = []
        exemplares_email = []
        alertas = []

        with transaction.atomic():
            for exemplar in exemplares:
                livro_id = exemplar['livro']['_id']
                
                e = Emprestimo(
                    usuario_id=usuario_id,
                    livro_id=livro_id,
                    exemplar_codigo=exemplar['codigo'],
                    exemplar_referencia=exemplar['referencia']
                )

                e.data_limite = data_limite_referencia if exemplar['referencia'] else data_limite
                e.save()

                reserva = reservas.get(livro_id)
                if reserva is not None:
                    reserva.emprestimo = e
                    reserva.save()

                emprestimos.append(e)

                titulo = exemplar['livro']['titulo']
                codigo = exemplar['codigo']
                dl = e.data_limite.strftime('%d/%m/%Y')

                exemplares_email.append({
                    'titulo': titulo,
                    'codigo': codigo,
                    'referencia': exemplar['referencia'],
                    'data_limite': dl
                })

                alertas.append({
                    'usuario_id': usuario_id,
                    'emprestimo_id': str(e._id),
                    'titulo': titulo,
                    'exemplar_codigo': codigo,
                    'data_limite': dl,
                })

            CatalogoService.call_exemplares_emprestados(codigos)

            agora = timezone.localtime()

            cls.call_enviar_comprovante_emprestimo({
                'usuario_id': usuario_id,
                'atendente_id': atendente_id,
                'data': agora.strftime('%d/%m/%Y'),
                'hora': agora.strftime('%H:%M:%S'),
                'exemplares': exemplares_email
            })
            cls.call_agendar_alertas_emprestimo(alertas)

            return emprestimos

    @classmethod
    def fetch_emprestimos_para_renovacao(cls, emprestimos_id, usuario_id):
        emprestimos = []
        usuarios = {}
        filtro = {}
        hoje = timezone.localdate()

        if usuario_id:
            filtro['usuario_id'] = usuario_id

        for e_id in emprestimos_id:
            filtro['_id'] = e_id
            
            emprestimo = Emprestimo.objects.filter(**filtro).first()
            if emprestimo is None:
                continue
            
            cls.validar_emprestimo_para_renovacao(emprestimo, hoje)

            usuario_id = str(emprestimo.usuario_id)
            if usuarios.get(usuario_id) is None:
                usuarios[usuario_id] = cls.buscar_usuario_renovacao(usuario_id, hoje)
            
            emprestimos.append(emprestimo)

        return emprestimos, usuarios

    @classmethod
    def validar_emprestimo_para_renovacao(cls, emprestimo, hoje):
        if emprestimo.data_devolucao is not None:
            raise APIException('Não é possível renovar empréstimo devolvido')

        if emprestimo.data_limite < hoje:
            raise APIException('Há empréstimos atrasados')

        if emprestimo.maximo_renovacoes:
            raise APIException('Há empréstimos com máximo de renovações')

        if emprestimo.exemplar_referencia:
            raise APIException('Não é possível renovar empréstimo de exemplar referência')

        if Reserva.objects.filter(
            livro_id=emprestimo.livro_id,
            emprestimo_id=None,
            cancelada=False,
            disponibilidade_retirada=None,
        ).exists():
            raise APIException('Existem reservas para esse exemplar, não é possível renovar o empréstimo')

    @classmethod
    def buscar_usuario_renovacao(cls, usuario_id, hoje):
        try:
            usuario = AutenticacaoService.consulta_usuario(usuario_id)
        except:
            raise APIException('Não foi possível obter informações do usuário')

        AutenticacaoService.check_usuario_suspenso(usuario_id, usuario['suspensao'], hoje)

        return usuario

    @classmethod
    def save_renovacoes(cls, emprestimos, usuarios, agente_id):
        agora = timezone.localtime()
        agora_data = agora.strftime('%d/%m/%Y')
        agora_hora = agora.strftime('%H:%M:%S')

        comprovantes = []

        with transaction.atomic():
            for emprestimo in emprestimos:
                usuario_id = str(emprestimo.usuario_id)

                perfil = usuarios[usuario_id]['perfil']
                emprestimo.quantidade_renovacoes += 1
                
                if emprestimo.quantidade_renovacoes >= perfil['quantidade_renovacoes']:
                    emprestimo.maximo_renovacoes = True
                
                nova_data = FeriadoService.calcular_data_limite(perfil['max_dias'])
                
                emprestimo.data_limite = nova_data
                
                Renovacao.objects.create(
                    emprestimo=emprestimo,
                    nova_data_limite=nova_data,
                    usuario_id=agente_id
                )

                emprestimo.save()

                comprovantes.append({
                    'usuario_id': usuario_id,
                    'livro_id': str(emprestimo.livro_id),
                    'data_limite': nova_data.strftime('%d/%m/%Y'),
                    'data': agora_data,
                    'hora': agora_hora,
                    'exemplar_codigo': emprestimo.exemplar_codigo,
                    'atendente_id': agente_id if agente_id != usuario_id else '' 
                })

            cls.call_enviar_comprovantes_renovacao(comprovantes)

            return {}

    @classmethod
    def emprestimo_avaliado(cls, emprestimo_id):
        Emprestimo.objects.filter(_id=emprestimo_id).update(
            avaliado=True,
            updated=timezone.localtime()
        )

    @classmethod
    def enviar_comprovante_emprestimo(cls, contexto):
        NotificacaoService.comprovante_emprestimo(contexto)

    @classmethod
    def enviar_comprovante_renovacao(cls, contexto):
        livro = CatalogoService.busca_livro(contexto['livro_id'], sem_exemplares=True)
        contexto['titulo'] = livro['titulo']
        NotificacaoService.comprovante_renovacao(contexto)

    @classmethod
    def call_enviar_comprovante_emprestimo(cls, contexto):
        try_to_send(
            cls.task_enviar_comprovante_emprestimo,
            args=[contexto],
            queue=CIRCULACAO_QUEUE
        )

    @classmethod
    def call_enviar_comprovantes_renovacao(cls, comprovantes):
        func = lambda x: ({ 'args': [x], 'queue': CIRCULACAO_QUEUE })
        ctxs = list(map(func, comprovantes))

        try:
            send_task_group(cls.task_enviar_comprovante_renovacao, ctxs)

        except:
            for ctx in ctxs:
                name = datetime_name(cls.task_enviar_comprovante_renovacao)
                ctx.update({
                    'name': name,
                    'task': cls.task_enviar_comprovante_renovacao,
                })

            save_batch_clocked_tasks(contexts=ctxs)

    @classmethod
    def checar_emprestimo(cls, contexto):
        e = Emprestimo.objects.filter(_id=contexto['emprestimo_id']).first()
        
        if not e:
            return

        if e.data_devolucao is not None:
            return

        if e.data_limite < timezone.localdate():
            NotificacaoService.alerta_emprestimo_atrasado(contexto)
        else:
            NotificacaoService.alerta_emprestimo_vencendo(contexto)

    @classmethod
    def agendar_alertas_emprestimo(cls, contexto):
        e_id = contexto['emprestimo_id']
        e = Emprestimo.objects.filter(_id=e_id).first()
        
        if not e:
            return

        data = e.data_limite
        hoje = timezone.localdate()
        dias = [-2, -1, 0, 1]

        with transaction.atomic():
            for dia in dias:
                d = data + timezone.timedelta(days=dia)
                if d <= hoje:
                    continue

                contexto['hoje'] = dia == 0

                name = datetime_name(cls.task_checar_emprestimo)

                dt = timezone.make_aware(
                    timezone.datetime(
                        year=d.year,
                        month=d.month,
                        day=d.day,
                        hour=9,
                        minute=30
                    )
                )

                save_clocked_task(
                    dt=dt, 
                    delay_seconds=0,
                    name=name,
                    task=cls.task_checar_emprestimo,
                    args=[contexto],
                    queue=CIRCULACAO_QUEUE
                )

    @classmethod
    def call_agendar_alertas_emprestimo(cls, contextos):
        func = lambda x: ({ 'args': [x], 'queue': CIRCULACAO_QUEUE })
        ctxs = list(map(func, contextos))

        try:
            send_task_group(cls.task_agendar_alertas_emprestimo, ctxs)

        except:
            for ctx in ctxs:
                name = datetime_name(cls.task_agendar_alertas_emprestimo)
                ctx.update({
                    'name': name,
                    'task': cls.task_agendar_alertas_emprestimo,
                })

            save_batch_clocked_tasks(contexts=ctxs)
