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
    _verificar_reserva
)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def marcar_exemplares_emprestados(usuario_id, codigos):
    _marcar_exemplares_emprestados(usuario_id, codigos)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def marcar_exemplares_devolvidos(usuario_id, codigos):
    _marcar_exemplares_devolvidos(usuario_id, codigos)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def usuarios_suspensos(usuario_id, usuarios):
    _usuarios_suspensos(usuario_id, usuarios)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def usuarios_abono(usuario_id, usuarios):
    _usuarios_abono(usuario_id, usuarios)

@shared_task(autoretry_for=(Exception,), max_retries=None, default_retry_delay=30)
def verificar_reserva(reserva_id):
    _verificar_reserva(reserva_id)
