from __future__ import absolute_import, unicode_literals

from celery import shared_task
from autenticacaoapp.tasks.usuario import (
    _usuarios_suspensos,
    _usuarios_abono
)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def usuarios_suspensos(usuarios):
    _usuarios_suspensos(usuarios)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def usuarios_abono(usuarios):
    _usuarios_abono(usuarios)
