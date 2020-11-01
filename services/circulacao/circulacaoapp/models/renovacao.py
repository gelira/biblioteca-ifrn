import uuid
from django.db import models

from .timestamped import TimestampedModel
from .emprestimo import Emprestimo

class Renovacao(TimestampedModel):
    emprestimo = models.ForeignKey(
        to=Emprestimo,
        on_delete=models.PROTECT,
        related_name='renovacoes'
    )
    data_renovacao = models.DateField(
        auto_now_add=True
    )
    nova_data_limite = models.DateField()
    usuario_id = models.UUIDField()

    class Meta:
        db_table = 'renovacoes'
        ordering = [
            'data_renovacao'
        ]
