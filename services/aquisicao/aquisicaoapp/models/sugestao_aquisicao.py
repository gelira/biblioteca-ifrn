import uuid
from django.db import models

from .timestamped import TimestampedModel
from .lista_sugestoes import ListaSugestoes

class SugestaoAquisicao(TimestampedModel):
    _id = models.UUIDField(
        unique=True, 
        editable=False, 
        default=uuid.uuid4
    )
    lista_sugestoes = models.ForeignKey(
        to=ListaSugestoes,
        on_delete=models.PROTECT,
        related_name='sugestoes',
        null=True
    )
    usuario_id = models.UUIDField()
    livro_id = models.UUIDField(
        null=True
    )
    titulo = models.CharField(
        max_length=100
    )
    autor_principal = models.CharField(
        max_length=100
    )
    autores_secundarios = models.CharField(
        max_length=200,
        blank=True
    )
    local_publicacao = models.CharField(
        max_length=100,
        blank=True
    )
    editora = models.CharField(
        max_length=100
    )
    ano_publicacao = models.CharField(
        max_length=10,
        blank=True
    )
    volume = models.CharField(
        max_length=10,
        blank=True
    )
    edicao = models.CharField(
        max_length=10,
        blank=True
    )
    isbn = models.CharField(
        max_length=20,
        blank=True
    )
    cdu = models.CharField(
        max_length=10,
        blank=True
    )
    cutter = models.CharField(
        max_length=20,
        blank=True
    )
    paginas = models.CharField(
        max_length=10,
        blank=True
    )
    comentario = models.TextField(
        blank=True
    )
    quantidade_curtidas = models.IntegerField(
        default=0
    )
    censurada = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'sugestoes_aquisicao'
        ordering = [
            '-quantidade_curtidas',
            'titulo',
        ]
