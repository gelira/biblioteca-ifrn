import os
import json
from celery import group
from django.utils import timezone
from django.db import transaction
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from rest_framework.exceptions import APIException

from circulacao.celery import app

from .. import exceptions
from ..models import Emprestimo
from .notificacao import NotificacaoService
from .catalogo import CatalogoService
from .reserva import ReservaService
from .feriado import FeriadoService

CIRCULACAO_QUEUE = os.getenv('CIRCULACAO_QUEUE')

class EmprestimoService:
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

            CatalogoService.exemplares_emprestados(codigos)

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
        app.send_task(
            'circulacao.enviar_comprovante_emprestimo',
            args=[contexto],
            queue=CIRCULACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def call_enviar_comprovantes_renovacao(cls, comprovantes):
        group([
            app.signature(
                'circulacao.enviar_comprovante_renovacao',
                args=[comprovante],
                queue=CIRCULACAO_QUEUE,
                ignore_result=True    
            ) for comprovante in comprovantes
        ])()

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

                clock = ClockedSchedule.objects.create(
                    clocked_time=timezone.make_aware(
                        timezone.datetime(
                            year=d.year,
                            month=d.month,
                            day=d.day,
                            hour=9,
                            minute=30
                        )
                    )
                )

                PeriodicTask.objects.create(
                    clocked=clock,
                    name=f'Alerta Empréstimo {e_id} ({dia})',
                    task='circulacao.checar_emprestimo',
                    args=json.dumps([contexto]),
                    queue=CIRCULACAO_QUEUE,
                    one_off=True
                )

    @classmethod
    def call_agendar_alertas_emprestimo(cls, contextos):
        group([
            app.signature(
                'circulacao.agendar_alertas_emprestimo',
                args=[contexto],
                queue=CIRCULACAO_QUEUE,
                ignore_result=True  
            ) for contexto in contextos
        ])()
