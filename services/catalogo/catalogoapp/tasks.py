from celery import shared_task, Task

from .services import LivroService

class BaseTask(Task):
    autoretry_for = [Exception]
    default_retry_delay = 30
    max_retries = None

class IgnoreResultTask(BaseTask):
    ignore_result = True

class MaxRetriesTask(IgnoreResultTask):
    max_retries = 10

@shared_task(name=LivroService.task_upload_foto_capa, base=MaxRetriesTask)
def upload_foto_capa(livro_id, livro_pk, foto_base64):
    LivroService.upload_foto_capa(livro_id, livro_pk, foto_base64)
