from __future__ import absolute_import, unicode_literals

from celery import shared_task
from catalogoapp.tasks.exemplar import (
    _exemplares_emprestados,
    _exemplares_devolvidos
)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def exemplares_emprestados(codigos):
    _exemplares_emprestados(codigos)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def exemplares_devolvidos(codigos):
    _exemplares_devolvidos(codigos)
