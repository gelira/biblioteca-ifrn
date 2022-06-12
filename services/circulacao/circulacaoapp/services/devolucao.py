import os
from celery import group
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import APIException

from circulacao.celery import app

from ..models import Emprestimo, Suspensao

from .autenticacao import AutenticacaoService
from .catalogo import CatalogoService
from .notificacao import NotificacaoService
from .reserva import ReservaService

CIRCULACAO_QUEUE = os.getenv('CIRCULACAO_QUEUE')

class DevolucaoService:
    @classmethod
    def get_emprestimos_para_devolucao(cls, emprestimos_id):
        qs = Emprestimo.objects.filter(
            _id__in=emprestimos_id, 
            data_devolucao=None
        )

        lista_emprestimos = list(qs)

        if len(lista_emprestimos) == 0:
            raise APIException('Nenhum empréstimo foi encontrado')

        return lista_emprestimos

    @classmethod
    def save_devolucoes(cls, emprestimos, atendente_id):
        agora = timezone.localtime()
        hoje = agora.date()
        data = agora.strftime('%d/%m/%Y')
        hora = agora.strftime('%H:%M:%S')
        
        suspensoes = {}
        codigos = []
        livros = []
        comprovantes = []

        with transaction.atomic():
            for emprestimo in emprestimos:
                diff = hoje - emprestimo.data_limite
                if diff.days > 0:
                    Suspensao.objects.create(
                        emprestimo=emprestimo,
                        usuario_id=emprestimo.usuario_id,
                        total_dias=diff.days
                    )

                    u_id = str(emprestimo.usuario_id)
                    if u_id not in suspensoes:
                        suspensoes[u_id] = 0
                    suspensoes[u_id] += diff.days

                codigos.append(emprestimo.exemplar_codigo)
                emprestimo.data_devolucao = hoje
                emprestimo.save()

                livro_id = str(emprestimo.livro_id)
                if livro_id not in livros:
                    livros.append(livro_id)

                comprovantes.append({
                    'usuario_id': str(emprestimo.usuario_id),
                    'atendente_id': atendente_id,
                    'livro_id': livro_id,
                    'atraso': diff.days,
                    'data': data,
                    'hora': hora,
                    'exemplar_codigo': emprestimo.exemplar_codigo,
                    'referencia': emprestimo.exemplar_referencia,
                })

            if suspensoes:
                AutenticacaoService.suspensoes(list(map(
                    lambda x: ({ 'usuario_id': x, 'dias': suspensoes[x] }), suspensoes)))

            CatalogoService.exemplares_devolvidos(codigos)
            
            cls.call_enviar_comprovantes_devolucao(comprovantes)
            ReservaService.call_proximas_reservas(livros)

        return {}

    @classmethod
    def enviar_comprovante_devolucao(cls, contexto):
        livro_id = contexto['livro_id']
        livro = CatalogoService.busca_livro(livro_id, sem_exemplares=True)

        contexto.update({
            'titulo': livro['titulo']
        })

        NotificacaoService.comprovante_devolucao(contexto)

    @classmethod
    def call_enviar_comprovantes_devolucao(cls, comprovantes):
        group([
            app.signature(
                'circulacao.enviar_comprovante_devolucao',
                args=[comprovante],
                queue=CIRCULACAO_QUEUE,
                ignore_result=True
            ) for comprovante in comprovantes
        ])()
