from django.db import models

from .livro import Livro

class Indexador(models.Model):
    livro = models.ForeignKey(
        to=Livro,
        on_delete=models.CASCADE,
        related_name='indexadores'
    )
    indexador = models.CharField(
        max_length=50
    )

    class Meta:
        db_table = 'indexadores'
        ordering = [
            'indexador'
        ]
