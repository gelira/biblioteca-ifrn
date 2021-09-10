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

class MaxRetriesTask(IgnoreResultTask):
    max_retries = 10

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

@shared_task(name='catalogo.upload_foto_capa', base=MaxRetriesTask)
def upload_foto_capa(livro_id, livro_pk, foto_base64):
    LivroService.upload_foto_capa(livro_id, livro_pk, foto_base64)

@shared_task(name='catalogo.atualizar_nota', base=IgnoreResultTask)
def atualizar_nota(livro_id, nota):
    LivroService.atualizar_nota(livro_id, nota)
