import os
from autenticacao.celery import app

NOTIFICACAO_QUEUE = os.getenv('NOTIFICACAO_QUEUE')

class NotificacaoService:
    @classmethod
    def salvar_contato(cls, usuario_id, data):
        app.send_task(
            'notificacao.salvar_contato',
            args=[usuario_id, data],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )
