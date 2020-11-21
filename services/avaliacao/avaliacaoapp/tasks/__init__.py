from __future__ import absolute_import, unicode_literals

from celery import shared_task
from avaliacaoapp.tasks.emprestimo import _emprestimo_avaliado

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def emprestimo_avaliado(usuario_id, emprestimo_id):
    _emprestimo_avaliado(usuario_id, emprestimo_id)
