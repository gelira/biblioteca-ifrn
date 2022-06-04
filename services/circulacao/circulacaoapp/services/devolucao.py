import os
from celery import group

from circulacao.celery import app

from .catalogo import CatalogoService
from .notificacao import NotificacaoService

CIRCULACAO_QUEUE = os.getenv('CIRCULACAO_QUEUE')

class DevolucaoService:
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
