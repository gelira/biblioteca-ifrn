import os
from circulacao.celery import app

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
    def comprovante_renovacao(cls, contexto):
        app.send_task(
            'notificacao.comprovante_renovacao',
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

    @classmethod
    def comprovante_reserva(cls, contexto):
        app.send_task(
            'notificacao.comprovante_reserva',
            args=[contexto],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )
    
    @classmethod
    def comprovante_reserva_cancelada(cls, contexto):
        app.send_task(
            'notificacao.comprovante_reserva_cancelada',
            args=[contexto],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def alerta_emprestimo_vencendo(cls, contexto):
        app.send_task(
            'notificacao.alerta_emprestimo_vencendo',
            args=[contexto],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def alerta_emprestimo_atrasado(cls, contexto):
        app.send_task(
            'notificacao.alerta_emprestimo_atrasado',
            args=[contexto],
            queue=NOTIFICACAO_QUEUE,
            ignore_result=True
        )
