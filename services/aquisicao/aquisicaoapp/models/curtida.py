from django.db import models

from .timestamped import TimestampedModel
from .sugestao_aquisicao import SugestaoAquisicao

class Curtida(TimestampedModel):
    sugestao_aquisicao = models.ForeignKey(
        to=SugestaoAquisicao,
        on_delete=models.PROTECT,
        related_name='curtidas'
    )
    usuario_id = models.UUIDField()
    aviso = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'curtidas'
        constraints = [
            models.UniqueConstraint(
                fields=['sugestao_aquisicao_id', 'usuario_id'], 
                name='curtida_unica'
            ),
        ]
