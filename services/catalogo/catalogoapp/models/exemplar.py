from django.db import models

from .livro import Livro

class Exemplar(models.Model):
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

    class Meta:
        db_table = 'exemplares'
