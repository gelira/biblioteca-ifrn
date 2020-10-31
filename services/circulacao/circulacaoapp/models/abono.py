import uuid
from django.db import models

from .timestamped import TimestampedModel

class Abono(TimestampedModel):
    _id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    usuario_id = models.UUIDField()
    justificativa = models.TextField()

    class Meta:
        db_table = 'abonos'
