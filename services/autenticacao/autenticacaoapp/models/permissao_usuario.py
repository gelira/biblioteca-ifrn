from django.db import models

from .timestamped import TimestampedModel
from .usuario import Usuario
from .permissao import Permissao

class PermissaoUsuario(TimestampedModel):
    permissao = models.ForeignKey(
        to=Permissao,
        on_delete=models.PROTECT,
        related_name='usuarios'
    )
    usuario = models.ForeignKey(
        to=Usuario,
        on_delete=models.PROTECT,
        related_name='permissoes'
    )

    class Meta:
        db_table = 'permissoes_usuarios'
