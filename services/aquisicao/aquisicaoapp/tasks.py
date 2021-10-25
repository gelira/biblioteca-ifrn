from celery import shared_task, Task

from .services import (
    SugestaoAquisicaoService,
    ListaSugestoesService,
)

class BaseTask(Task):
    autoretry_for = [Exception]
    default_retry_delay = 30
    max_retries = None

class IgnoreResultTask(BaseTask):
    ignore_result = True

@shared_task(name='aquisicao.enviar_alertas_lista', base=IgnoreResultTask)
def enviar_alertas_lista(lista_sugestoes_id):
    ListaSugestoesService.enviar_alertas_lista(lista_sugestoes_id)

@shared_task(name='aquisicao.enviar_alertas_sugestao', base=IgnoreResultTask)
def enviar_alertas_sugestao(contexto):
    SugestaoAquisicaoService.enviar_alertas_sugestao(contexto)

@shared_task(name='aquisicao.enviar_alerta_sugestao', base=IgnoreResultTask)
def enviar_alerta_sugestao(contexto):
    SugestaoAquisicaoService.enviar_alerta_sugestao(contexto)
