from __future__ import absolute_import, unicode_literals

from django.db import transaction
from django.utils import timezone
from circulacaoapp.models import Reserva, Data
from circulacaoapp.utils import calcular_data_limite

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
