from __future__ import absolute_import, unicode_literals

from celery import shared_task
from circulacaoapp.tasks.emprestimo import (
    _marcar_exemplares_emprestados,
    _marcar_exemplares_devolvidos
)
from circulacaoapp.tasks.usuario import (
    _usuarios_suspensos,
    _usuarios_abono
)
from circulacaoapp.tasks.reserva import (
    _verificar_reserva,
    _verificar_reservas
)
from circulacaoapp.tasks.devolucao import (
    _enviar_comprovantes_devolucao
)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def marcar_exemplares_emprestados(codigos):
    _marcar_exemplares_emprestados(codigos)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def marcar_exemplares_devolvidos(codigos):
    _marcar_exemplares_devolvidos(codigos)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def usuarios_suspensos(usuarios):
    _usuarios_suspensos(usuarios)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def usuarios_abono(usuarios):
    _usuarios_abono(usuarios)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def verificar_reserva(reserva_id):
    _verificar_reserva(reserva_id)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def enviar_comprovantes_devolucao(comprovantes):
    _enviar_comprovantes_devolucao(comprovantes)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def verificar_reservas():
    _verificar_reservas()
