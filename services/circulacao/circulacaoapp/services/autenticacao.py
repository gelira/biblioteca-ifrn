import os
from celery import group
from circulacao.celery import app

AUTENTICACAO_QUEUE = os.getenv('AUTENTICACAO_QUEUE')

class AutenticacaoService:
    @classmethod
    def autenticar_usuario(cls, matricula, senha):
        data_token = cls.login_suap(matricula, senha)
        data_verify = cls.verificar_token(data_token['token'])
        return cls.informacoes_usuario(data_verify['user_id'])

    @classmethod
    def login_suap(cls, username, password):
        task = app.send_task(
            'autenticacao.login_suap', 
            args=[username, password], 
            queue=AUTENTICACAO_QUEUE
        )
        return task.get()

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
        return task.get(disable_sync_subtasks=False)

    @classmethod
    def suspensoes(cls, suspensoes):
        tasks = [
            app.signature(
                'autenticacao.suspensao', 
                args=[u, suspensoes[u]], 
                ignore_resut=True, 
                queue=AUTENTICACAO_QUEUE
            ) for u in suspensoes
        ]
        group(tasks)()
    
    @classmethod
    def abono_suspensoes(cls, usuarios):
        tasks = [
            app.signature(
                'autenticacao.abono_suspensao', 
                args=[u, usuarios[u]], 
                ignore_resut=True, 
                queue=AUTENTICACAO_QUEUE
            ) for u in usuarios
        ]
        group(tasks)()
