from __future__ import absolute_import, unicode_literals

import os
from django.db import transaction
from django.utils import timezone
from circulacao.celery import app
from circulacaoapp.models import Reserva, Data
from circulacaoapp.utils import calcular_data_limite

PROJECT_NAME = os.getenv('PROJECT_NAME')

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
        app.send_task('circulacaoapp.tasks.verificar_reserva', [str(proxima_reserva._id)], eta=eta, queue=PROJECT_NAME)

def _verificar_reservas():
    data = timezone.localdate() - timezone.timedelta(days=1)
    
    if data.weekday() > 4: 
        # Sábado ou Domingo
        return

    if Data.objects.filter(
        dia=data.day, 
        mes=data.month, 
        ano=data.year
    ).exists():
        return

    reservas = Reserva.objects.filter(
        disponibilidade_retirada__lt=data,
        emprestimo_id=None,
        cancelada=False
    ).all()

    with transaction.atomic():
        for reserva in reservas:
            reserva.cancelada = True
            reserva.save()

            proxima_reserva = Reserva.objects.filter(
                disponibilidade_retirada=None,
                livro_id=reserva.livro_id,
                emprestimo_id=None,
                cancelada=False
            ).first()

            if proxima_reserva is not None:
                proxima_reserva.disponibilidade_retirada = calcular_data_limite(1)
                proxima_reserva.save()
