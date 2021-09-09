import os
from circulacao.celery import app

CIRCULACAO_QUEUE = os.getenv('PROJECT_NAME')
NOTIFICACAO_QUEUE = os.getenv('NOTIFICACAO_QUEUE')

class NotificacaoService:
    @classmethod
    def comprovante_emprestimo(cls, contexto):
        app.send_task(
            'notificacao.comprovante_emprestimo',
            args=[contexto],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def comprovante_devolucao(cls, contexto):
        app.send_task(
            'notificacao.comprovante_devolucao',
            args=[contexto],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def reserva_disponivel(cls, contexto):
        app.send_task(
            'notificacao.reserva_disponivel',
            args=[contexto],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def reserva_cancelada(cls, contexto):
        app.send_task(
            'notificacao.reserva_cancelada',
            args=[contexto],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )
