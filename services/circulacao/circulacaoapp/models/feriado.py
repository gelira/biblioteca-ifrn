import uuid
from django.db import models

from .timestamped import TimestampedModel

class Feriado(TimestampedModel):
    descricao = models.CharField(
        max_length=200
    )

    class Meta:
        db_table = 'feriados'
