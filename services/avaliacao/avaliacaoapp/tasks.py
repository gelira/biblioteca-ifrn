from celery import shared_task, Task

from .services import ModeracaoService

class BaseTask(Task):
    autoretry_for = [Exception]
    default_retry_delay = 30
    max_retries = None

class IgnoreResultTask(BaseTask):
    ignore_result = True

@shared_task(name='avaliacao.avaliacao_moderada', base=IgnoreResultTask)
def avaliacao_moderada(contexto):
    ModeracaoService.avaliacao_moderada(contexto)

@shared_task(name='avaliacao.avaliacao_publicada', base=IgnoreResultTask)
def avaliacao_publicada(contexto):
    ModeracaoService.avaliacao_publicada(contexto)
