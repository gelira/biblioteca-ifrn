import os

from .base import try_to_send

NOTIFICACAO_QUEUE = os.getenv('NOTIFICACAO_QUEUE')

class NotificacaoService:
    task_comprovante_emprestimo = 'notificacao.comprovante_emprestimo'
    task_comprovante_devolucao = 'notificacao.comprovante_devolucao'
    task_comprovante_renovacao = 'notificacao.comprovante_renovacao'
    task_reserva_disponivel = 'notificacao.reserva_disponivel'
    task_reserva_cancelada = 'notificacao.reserva_cancelada'
    task_comprovante_reserva = 'notificacao.comprovante_reserva'
    task_comprovante_reserva_cancelada = 'notificacao.comprovante_reserva_cancelada'
    task_alerta_emprestimo_vencendo = 'notificacao.alerta_emprestimo_vencendo'
    task_alerta_emprestimo_atrasado = 'notificacao.alerta_emprestimo_atrasado'

    @classmethod
    def comprovante_emprestimo(cls, contexto):
        try_to_send(
            cls.task_comprovante_emprestimo, 
            args=[contexto], 
            queue=NOTIFICACAO_QUEUE
        )

    @classmethod
    def comprovante_devolucao(cls, contexto):
        try_to_send(
            cls.task_comprovante_devolucao, 
            args=[contexto], 
            queue=NOTIFICACAO_QUEUE
        )

    @classmethod
    def comprovante_renovacao(cls, contexto):
        try_to_send(
            cls.task_comprovante_renovacao, 
            args=[contexto], 
            queue=NOTIFICACAO_QUEUE
        )

    @classmethod
    def reserva_disponivel(cls, contexto):
        try_to_send(
            cls.task_reserva_disponivel, 
            args=[contexto], 
            queue=NOTIFICACAO_QUEUE
        )

    @classmethod
    def reserva_cancelada(cls, contexto):
        try_to_send(
            cls.task_reserva_cancelada, 
            args=[contexto], 
            queue=NOTIFICACAO_QUEUE
        )

    @classmethod
    def comprovante_reserva(cls, contexto):
        try_to_send(
            cls.task_comprovante_reserva, 
            args=[contexto], 
            queue=NOTIFICACAO_QUEUE
        )
    
    @classmethod
    def comprovante_reserva_cancelada(cls, contexto):
        try_to_send(
            cls.task_comprovante_reserva_cancelada, 
            args=[contexto], 
            queue=NOTIFICACAO_QUEUE
        )

    @classmethod
    def alerta_emprestimo_vencendo(cls, contexto):
        try_to_send(
            cls.task_alerta_emprestimo_vencendo, 
            args=[contexto], 
            queue=NOTIFICACAO_QUEUE
        )

    @classmethod
    def alerta_emprestimo_atrasado(cls, contexto):
        try_to_send(
            cls.task_alerta_emprestimo_atrasado, 
            args=[contexto], 
            queue=NOTIFICACAO_QUEUE
        )
