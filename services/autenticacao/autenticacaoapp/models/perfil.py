from django.db import models

from .timestamped import TimestampedModel

class Perfil(TimestampedModel):
    descricao = models.CharField(max_length=100)
    padrao = models.BooleanField()
    max_livros = models.PositiveIntegerField()
    max_dias = models.PositiveIntegerField()

    class Meta:
        db_table = 'perfis'
