from django.db import models
from django.conf import settings
import uuid

class Usuario(models.Model):
    _id = models.UUIDField(
        unique=True, 
        editable=False, 
        default=uuid.uuid4)
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT)
    nome = models.CharField(max_length=150)
    nome_completo = models.CharField(max_length=150)
    email_institucional = models.EmailField()
    email_pessoal = models.EmailField(blank=True)
    vinculo = models.CharField(max_length=20)
    url_foto = models.CharField(max_length=150)

    class Meta:
        db_table = 'usuarios'
