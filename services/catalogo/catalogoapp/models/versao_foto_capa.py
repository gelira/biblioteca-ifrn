from django.db import models

from .timestamped import TimestampedModel
from .foto_capa import FotoCapa

class VersaoFotoCapa(TimestampedModel):
    foto_capa = models.ForeignKey(
        to=FotoCapa,
        on_delete=models.PROTECT,
        related_name='versoes'
    )
    version_id = models.CharField(
        max_length=100
    )
    atual = models.BooleanField(
        default=True
    )

    class Meta:
        db_table = 'versoes_foto_capa'
        ordering = [
            'created'
        ]
