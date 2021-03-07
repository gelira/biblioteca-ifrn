from __future__ import absolute_import, unicode_literals

from celery import shared_task
from notificacaoapp.tasks.mensagens import (
    _comprovante_emprestimo,
    _comprovante_devolucao
)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def comprovante_emprestimo(contexto, emails):
    _comprovante_emprestimo(contexto, emails)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def comprovante_devolucao(contexto, emails):
    _comprovante_devolucao(contexto, emails)
