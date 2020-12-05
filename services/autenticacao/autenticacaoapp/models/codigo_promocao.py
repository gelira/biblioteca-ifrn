from django.db import models

from .timestamped import TimestampedModel
from .usuario import Usuario

class CodigoPromocao(TimestampedModel):
    codigo = models.CharField(
        max_length=20
    )
    codigo_utilizado = models.CharField(
        max_length=20,
        blank=True
    )
    validade = models.DateTimeField()
    usuario = models.ForeignKey(
        to=Usuario,
        on_delete=models.PROTECT,
        related_name='codigos_promocao'
    )
    bolsista = models.ForeignKey(
        to=Usuario,
        on_delete=models.PROTECT,
        related_name='codigos_promocao_utilizados',
        null=True
    )

    class Meta:
        db_table = 'codigos_promocao'
