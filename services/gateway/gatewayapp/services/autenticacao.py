import os
from gateway.celery import app

AUTENTICACAO_QUEUE = os.getenv('AUTENTICACAO_QUEUE')

class AutenticacaoService:
    @classmethod
    def verificar_token(cls, token):
        task = app.send_task(
            'autenticacao.verificar_token', 
            args=[token], 
            queue=AUTENTICACAO_QUEUE
        )
        return task.get()

    @classmethod
    def informacoes_usuario(cls, usuario_id):
        task = app.send_task(
            'autenticacao.informacoes_usuario', 
            args=[usuario_id], 
            queue=AUTENTICACAO_QUEUE
        )
        return task.get()
