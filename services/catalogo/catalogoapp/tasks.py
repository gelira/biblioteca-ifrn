from celery import shared_task, Task

from .services import (
    ExemplarService,
    LivroService
)

class BaseTask(Task):
    autoretry_for = [Exception]
    default_retry_delay = 30
    max_retries = None

class IgnoreResultTask(BaseTask):
    ignore_result = True

@shared_task(name='catalogo.exemplares_emprestados', base=IgnoreResultTask)
def exemplares_emprestados(codigos):
    ExemplarService.exemplares_emprestados(codigos)

@shared_task(name='catalogo.exemplares_devolvidos', base=IgnoreResultTask)
def exemplares_devolvidos(codigos):
    ExemplarService.exemplares_devolvidos(codigos)

@shared_task(name='catalogo.consulta_codigo_exemplar', base=BaseTask)
def consulta_codigo_exemplar(codigo):
    return ExemplarService.consulta_codigo_exemplar(codigo)

@shared_task(name='catalogo.busca_livro', base=BaseTask)
def busca_livro(livro_id, **kwargs):
    return LivroService.busca_livro(livro_id, **kwargs)
