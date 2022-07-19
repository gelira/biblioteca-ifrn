import uuid
from django.db import models

from .timestamped import TimestampedModel
from .tag import Tag

class Avaliacao(TimestampedModel):
    _id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    tags = models.ManyToManyField(
        to=Tag,
        db_table='avaliacoes_tags'
    )
    usuario_id = models.UUIDField()
    emprestimo_id = models.UUIDField()
    livro_id = models.UUIDField()
    nota = models.PositiveIntegerField()
    comentario = models.TextField(
        blank=True
    )
    censurada = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'avaliacoes'
        ordering = [
            '-created'
        ]
