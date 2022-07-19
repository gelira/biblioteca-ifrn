from django.db import models

from .timestamped import TimestampedModel
from .feriado import Feriado

class Data(TimestampedModel):
    feriado = models.ForeignKey(
        to=Feriado,
        on_delete=models.CASCADE,
        related_name='datas'
    )
    dia = models.PositiveIntegerField()
    mes = models.PositiveIntegerField()
    ano = models.PositiveIntegerField()

    class Meta:
        db_table = 'datas'
