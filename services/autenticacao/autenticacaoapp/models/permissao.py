from django.db import models

from .timestamped import TimestampedModel

class Permissao(TimestampedModel):
    codigo = models.CharField(
        max_length=100,
        unique=True
    )
    descricao = models.CharField(
        max_length=100
    )

    class Meta:
        db_table = 'permissoes'
