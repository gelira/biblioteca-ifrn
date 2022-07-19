from django.db import models

from .timestamped import TimestampedModel
from .livro import Livro

class Exemplar(TimestampedModel):
    livro = models.ForeignKey(
        to=Livro,
        on_delete=models.CASCADE,
        related_name='exemplares'
    )
    codigo = models.CharField(
        max_length=8,
        editable=False,
        unique=True
    )
    referencia = models.BooleanField(
        default=False
    )
    disponivel = models.BooleanField(
        default=True
    )
    ativo = models.BooleanField(
        default=True
    )

    class Meta:
        db_table = 'exemplares'
