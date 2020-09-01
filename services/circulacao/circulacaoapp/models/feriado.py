import uuid
from django.db import models

class Feriado(models.Model):
    descricao = models.CharField(
        max_length=200
    )

    class Meta:
        db_table = 'feriados'
