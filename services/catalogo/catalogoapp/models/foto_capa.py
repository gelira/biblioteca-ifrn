from django.db import models

from .timestamped import TimestampedModel
from .livro import Livro

class FotoCapa(TimestampedModel):
    livro = models.OneToOneField(
        to=Livro,
        on_delete=models.PROTECT,
        related_name='foto_capa'
    )
    region = models.CharField(
        max_length=100
    )
    bucket = models.CharField(
        max_length=100
    )
    key = models.CharField(
        max_length=100
    )

    class Meta:
        db_table = 'fotos_capas'
        ordering = [
            'created'
        ]
