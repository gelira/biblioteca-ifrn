from django.db import models

from .livro import Livro

class LocalizacaoFisica(models.Model):
    livro = models.ForeignKey(
        to=Livro,
        on_delete=models.CASCADE,
        related_name='localizacoes'
    )
    localizacao = models.CharField(
        max_length=200
    )
    ativo = models.BooleanField(
        default=True
    )

    class Meta:
        db_table = 'localizacoes_fisicas'
