from __future__ import absolute_import, unicode_literals

from django.db import transaction
from django.utils import timezone
from circulacao.celery import app
from circulacaoapp.models import Reserva
from circulacaoapp.utils import calcular_data_limite

def _verificar_reserva(reserva_id):
    with transaction.atomic():
        reserva = Reserva.objects.filter(
            _id=reserva_id,
            emprestimo_id=None,
            cancelada=False
        ).first()
        if reserva is None:
            return

        reserva.cancelada = True
        reserva.save()

        proxima_reserva = Reserva.objects.filter(
            disponibilidade_retirada=None,
            livro_id=reserva.livro_id,
            emprestimo_id=None,
            cancelada=False
        ).first()
        if proxima_reserva is None:
            return

        proxima_reserva.disponibilidade_retirada = calcular_data_limite(1)
        proxima_reserva.save()

        data = proxima_reserva.disponibilidade_retirada + timezone.timedelta(days=1)
        eta = timezone.datetime(
            year=data.year,
            month=data.month,
            day=data.day,
            hour=1,
            minute=36,
            tzinfo=timezone.pytz.timezone('America/Sao_Paulo')
        )
        app.send_task('circulacaoapp.tasks.verificar_reserva', [str(proxima_reserva._id)], eta=eta)
