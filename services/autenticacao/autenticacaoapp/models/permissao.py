from django.db import models

class Permissao(models.Model):
    codigo = models.CharField(
        max_length=100,
        unique=True
    )
    descricao = models.CharField(
        max_length=100
    )

    class Meta:
        db_table = 'permissoes'
