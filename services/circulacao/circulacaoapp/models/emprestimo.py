import uuid
from django.db import models

from .timestamped import TimestampedModel

class Emprestimo(TimestampedModel):
    _id = models.UUIDField(
        unique=True, 
        editable=False, 
        default=uuid.uuid4
    )
    usuario_id = models.UUIDField()
    livro_id = models.UUIDField()
    exemplar_codigo = models.CharField(
        max_length=20
    )
    data_emprestimo = models.DateField(
        auto_now_add=True
    )
    data_limite = models.DateField()
    data_devolucao = models.DateField(
        null=True
    )
    quantidade_renovacoes = models.PositiveIntegerField(
        default=0
    )
    avaliado = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'emprestimos'
        ordering = [
            'data_emprestimo'
        ]
