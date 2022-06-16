import os

from .base import (
    send_task, 
    datetime_name, 
    save_clocked_task
)

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
        cls.try_to_send(cls.task_comprovante_emprestimo, [contexto])

    @classmethod
    def comprovante_devolucao(cls, contexto):
        cls.try_to_send(cls.task_comprovante_devolucao, [contexto])

    @classmethod
    def comprovante_renovacao(cls, contexto):
        cls.try_to_send(cls.task_comprovante_renovacao, [contexto])

    @classmethod
    def reserva_disponivel(cls, contexto):
        cls.try_to_send(cls.task_reserva_disponivel, [contexto])

    @classmethod
    def reserva_cancelada(cls, contexto):
        cls.try_to_send(cls.task_reserva_cancelada, [contexto])

    @classmethod
    def comprovante_reserva(cls, contexto):
        cls.try_to_send(cls.task_comprovante_reserva, [contexto])
    
    @classmethod
    def comprovante_reserva_cancelada(cls, contexto):
        cls.try_to_send(cls.task_comprovante_reserva_cancelada, [contexto])

    @classmethod
    def alerta_emprestimo_vencendo(cls, contexto):
        cls.try_to_send(cls.task_alerta_emprestimo_vencendo, [contexto])

    @classmethod
    def alerta_emprestimo_atrasado(cls, contexto):
        cls.try_to_send(cls.task_alerta_emprestimo_atrasado, [contexto])

    @classmethod
    def try_to_send(cls, task_name, args):
        ctx = {
            'args': args,
            'queue': NOTIFICACAO_QUEUE,
            'ignore_result': True
        }

        try:
            send_task(task_name, **ctx)

        except:
            name = datetime_name(task_name)
            ctx.pop('ignore_result', None)
            ctx.update({
                'name': name,
                'task': task_name,
                'headers': { 'periodic_task_name': name },
                'one_off': True
            })
            
            save_clocked_task(**ctx)
