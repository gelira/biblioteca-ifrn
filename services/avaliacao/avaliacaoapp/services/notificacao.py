import os
from avaliacao.celery import app

NOTIFICACAO_QUEUE = os.getenv('NOTIFICACAO_QUEUE')

class NotificacaoService:
    @classmethod
    def avaliacao_moderada(cls, contexto):
        app.send_task(
            'notificacao.avaliacao_moderada',
            args=[contexto],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def avaliacao_publicada(cls, contexto):
        app.send_task(
            'notificacao.avaliacao_publicada',
            args=[contexto],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )
