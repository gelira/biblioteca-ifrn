from __future__ import absolute_import, unicode_literals

from celery import shared_task
from circulacaoapp.tasks.emprestimo import (
    _emprestimo_avaliado
)
from circulacaoapp.tasks.reserva import (
    _verificar_reservas,
    _enviar_reservas_disponiveis
)
from circulacaoapp.tasks.devolucao import (
    _enviar_comprovantes_devolucao
)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def enviar_comprovantes_devolucao(comprovantes):
    _enviar_comprovantes_devolucao(comprovantes)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def verificar_reservas():
    _verificar_reservas()

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def emprestimo_avaliado(emprestimo_id):
    _emprestimo_avaliado(emprestimo_id)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def enviar_reservas_disponiveis(comprovantes):
    _enviar_reservas_disponiveis(comprovantes)
