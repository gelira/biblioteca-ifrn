import os
from aquisicao.celery import app

NOTIFICACAO_QUEUE = os.getenv('NOTIFICACAO_QUEUE')

class NotificacaoService:
    @classmethod
    def alerta_sugestao_listada(cls, contexto):
        app.send_task(
            'notificacao.alerta_sugestao_listada',
            args=[contexto],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )
