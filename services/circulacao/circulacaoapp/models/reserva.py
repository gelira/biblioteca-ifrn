import uuid
from django.db import models

from .timestamped import TimestampedModel
from .emprestimo import Emprestimo

class Reserva(TimestampedModel):
    _id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    emprestimo = models.OneToOneField(
        to=Emprestimo,
        on_delete=models.PROTECT,
        null=True
    )
    usuario_id = models.UUIDField()
    livro_id = models.UUIDField()
    disponibilidade_retirada = models.DateTimeField(
        null=True
    )
    cancelada = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'reservas'
        ordering = [
            'created'
        ]
