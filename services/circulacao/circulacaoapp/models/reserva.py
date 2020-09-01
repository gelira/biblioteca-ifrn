import uuid
from django.db import models

from .emprestimo import Emprestimo

class Reserva(models.Model):
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
    momento = models.DateTimeField(
        auto_now_add=True
    )
    disponivel = models.DateTimeField(
        null=True
    )
    cancelada = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'reservas'
        ordering = [
            '-momento'
        ]
