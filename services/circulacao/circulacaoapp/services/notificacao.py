import os
from circulacao.celery import app

CIRCULACAO_QUEUE = os.getenv('PROJECT_NAME')
NOTIFICACAO_QUEUE = os.getenv('NOTIFICACAO_QUEUE')

class NotificacaoService:
    @classmethod
    def comprovante_emprestimo(cls, contexto, emails):
        app.send_task(
            'notificacao.comprovante_emprestimo',
            args=[contexto, emails],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def comprovante_devolucao(cls, contexto, emails):
        app.send_task(
            'notificacao.comprovante_devolucao',
            args=[contexto, emails],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def reserva_disponivel(cls, contexto, emails):
        app.send_task(
            'notificacao.reserva_disponivel',
            args=[contexto, emails],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def reserva_cancelada(cls, contexto, emails):
        app.send_task(
            'notificacao.reserva_cancelada',
            args=[contexto, emails],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )
