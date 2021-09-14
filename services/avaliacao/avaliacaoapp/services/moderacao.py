import os
from avaliacao.celery import app

from .catalogo import CatalogoService
from .notificacao import NotificacaoService

AVALIACAO_QUEUE = os.getenv('PROJECT_NAME')

class ModeracaoService:
    @classmethod
    def load_livro_info(cls, contexto):
        livro = CatalogoService.busca_livro(contexto['livro_id'])
        contexto['titulo'] = livro['titulo']
        return contexto

    @classmethod
    def avaliacao_moderada(cls, contexto):
        contexto = cls.load_livro_info(contexto)
        NotificacaoService.avaliacao_moderada(contexto)

    @classmethod
    def avaliacao_publicada(cls, contexto):
        contexto = cls.load_livro_info(contexto)
        NotificacaoService.avaliacao_publicada(contexto)

    @classmethod
    def call_avaliacao_moderada(cls, contexto):
        app.send_task(
            'avaliacao.avaliacao_moderada',
            args=[contexto],
            queue=AVALIACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def call_avaliacao_publicada(cls, contexto):
        app.send_task(
            'avaliacao.avaliacao_publicada',
            args=[contexto],
            queue=AVALIACAO_QUEUE,
            ignore_result=True
        )
