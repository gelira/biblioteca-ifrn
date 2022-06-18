from celery import shared_task, Task

from .services import (
    ModeracaoService, 
    CatalogoService,
    CirculacaoService
)

class BaseTask(Task):
    autoretry_for = [Exception]
    default_retry_delay = 60
    max_retries = None

class IgnoreResultTask(BaseTask):
    ignore_result = True

@shared_task(name=CatalogoService.task_atualizar_nota, base=IgnoreResultTask)
def atualizar_nota(livro_id, nota):
    CatalogoService.atualizar_nota(livro_id, nota)

@shared_task(name=CirculacaoService.task_emprestimo_avaliado, base=IgnoreResultTask)
def emprestimo_avaliado(emprestimo_id):
    CirculacaoService.emprestimo_avaliado(emprestimo_id)

@shared_task(name='avaliacao.avaliacao_moderada', base=IgnoreResultTask)
def avaliacao_moderada(contexto):
    ModeracaoService.avaliacao_moderada(contexto)

@shared_task(name='avaliacao.avaliacao_publicada', base=IgnoreResultTask)
def avaliacao_publicada(contexto):
    ModeracaoService.avaliacao_publicada(contexto)
