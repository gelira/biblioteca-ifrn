import os
from celery import group
from rest_framework.exceptions import APIException

from circulacao.celery import app

from ..models import Emprestimo

from .catalogo import CatalogoService
from .notificacao import NotificacaoService

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
