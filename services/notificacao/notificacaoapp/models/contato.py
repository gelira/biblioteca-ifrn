from django.db import models

from .timestamped import TimestampedModel

class Contato(TimestampedModel):
    usuario_id = models.UUIDField()
    nome = models.CharField(max_length=150)
    matricula = models.CharField(max_length=150)
    email_institucional = models.EmailField()
    email_pessoal = models.EmailField(blank=True)

    class Meta:
        db_table = 'contatos'
