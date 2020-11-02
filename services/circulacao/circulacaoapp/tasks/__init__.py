from __future__ import absolute_import, unicode_literals

from celery import shared_task
from circulacaoapp.tasks.emprestimo import (
    _marcar_exemplares_emprestados,
    _marcar_exemplares_devolvidos
)
from circulacaoapp.tasks.usuario import _usuarios_suspensos

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def marcar_exemplares_emprestados(usuario_id, codigos):
    try:
        _marcar_exemplares_emprestados(usuario_id, codigos)
    except Exception as e:
        raise self.retry(exc=e, countdown=10)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def marcar_exemplares_devolvidos(usuario_id, codigos):
    try:
        _marcar_exemplares_devolvidos(usuario_id, codigos)
    except Exception as e:
        raise self.retry(exc=e, countdown=10)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def usuarios_suspensos(usuario_id, usuarios):
    try:
        _usuarios_suspensos(usuario_id, usuarios)
    except Exception as e:
        raise self.retry(exc=e, countdown=10)
