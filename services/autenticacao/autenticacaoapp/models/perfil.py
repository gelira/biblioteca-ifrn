from django.db import models

class Perfil(models.Model):
    descricao = models.CharField(max_length=100)
    padrao = models.BooleanField()
    max_livros = models.PositiveIntegerField()
    max_dias = models.PositiveIntegerField()

    class Meta:
        db_table = 'perfis'
