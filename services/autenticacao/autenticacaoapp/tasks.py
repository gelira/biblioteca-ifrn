from celery import shared_task, Task

from .services import (
    AutenticacaoService, 
    UsuarioService,
    TokenService
)

class BaseTask(Task):
    autoretry_for = [Exception]
    default_retry_delay = 30
    max_retries = None

class IgnoreResultTask(BaseTask):
    ignore_result = True

@shared_task(name='autenticacao.verificar_token')
def verificar_token(token):
    return TokenService.verificar_token(token)

@shared_task(name='autenticacao.login_suap')
def login_suap(username, password):
    return AutenticacaoService.login_suap(username, password)

@shared_task(name='autenticacao.informacoes_usuario')
def informacoes_usuario(usuario_id):
    return AutenticacaoService.informacoes_usuario(usuario_id)

@shared_task(name='autenticacao.consulta_usuario')
def consulta_usuario(matricula):
    return AutenticacaoService.consulta_usuario(matricula)

@shared_task(name='autenticacao.suspensao', base=IgnoreResultTask)
def suspensao(usuario_id, dias):
    UsuarioService.suspensao(usuario_id, dias)

@shared_task(name='autenticacao.abono_suspensao', base=IgnoreResultTask)
def abono_suspensao(usuario_id, dias):
    UsuarioService.abono_suspensao(usuario_id, dias)
