import uuid
from django.db import models

from .timestamped import TimestampedModel
from .emprestimo import Emprestimo
from .abono import Abono

class Suspensao(TimestampedModel):
    _id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    emprestimo = models.ForeignKey(
        to=Emprestimo,
        on_delete=models.PROTECT,
        related_name='suspensoes'
    )
    abono = models.ForeignKey(
        to=Abono,
        on_delete=models.PROTECT,
        related_name='suspensoes',
        null=True
    )
    usuario_id = models.UUIDField()
    total_dias = models.PositiveIntegerField()

    class Meta:
        db_table = 'suspensoes'
