import uuid
from django.db import models

from .timestamped import TimestampedModel

class ListaSugestoes(TimestampedModel):
    _id = models.UUIDField(
        unique=True, 
        editable=False, 
        default=uuid.uuid4
    )
    descricao = models.CharField(
        max_length=100
    )

    class Meta:
        db_table = 'listas_sugestoes'
        ordering = [
            '-created'
        ]
