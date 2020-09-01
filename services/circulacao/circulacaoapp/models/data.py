from django.db import models

from .feriado import Feriado

class Data(models.Model):
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
