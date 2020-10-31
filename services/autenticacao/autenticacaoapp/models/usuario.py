from django.db import models
from django.conf import settings
import uuid

from .timestamped import TimestampedModel
from .perfil import Perfil

class Usuario(TimestampedModel):
    _id = models.UUIDField(
        unique=True, 
        editable=False, 
        default=uuid.uuid4
    )
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT
    )
    perfil = models.ForeignKey(
        to=Perfil,
        on_delete=models.SET_NULL,
        related_name='usuarios',
        null=True
    )
    nome = models.CharField(max_length=150)
    nome_completo = models.CharField(max_length=150)
    email_institucional = models.EmailField()
    email_pessoal = models.EmailField(blank=True)
    vinculo = models.CharField(max_length=20)
    url_foto = models.CharField(max_length=150)

    class Meta:
        db_table = 'usuarios'
