import uuid
from django.db import models

from .emprestimo import Emprestimo

class Renovacao(models.Model):
    emprestimo = models.ForeignKey(
        to=Emprestimo,
        on_delete=models.PROTECT,
        related_name='renovacoes'
    )
    data_renovacao = models.DateField(
        auto_now_add=True
    )
    nova_data_limite = models.DateField()
    agente = models.CharField(
        max_length=100
    )

    class Meta:
        db_table = 'renovacoes'
        ordering = [
            'data_renovacao'
        ]
