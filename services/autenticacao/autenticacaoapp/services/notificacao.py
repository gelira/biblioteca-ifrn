import os

from .base import try_to_send

NOTIFICACAO_QUEUE = os.getenv('NOTIFICACAO_QUEUE')

class NotificacaoService:
    task_salvar_contato = 'notificacao.salvar_contato'

    @classmethod
    def call_salvar_contato(cls, usuario_id, data):
        try_to_send(
            cls.task_salvar_contato,
            args=[usuario_id, data],
            queue=NOTIFICACAO_QUEUE
        )
