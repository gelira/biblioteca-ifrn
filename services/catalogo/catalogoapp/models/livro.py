from django.db import models

import uuid

class Livro(models.Model):
    _id = models.UUIDField(
        unique=True, 
        editable=False, 
        default=uuid.uuid4
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
        max_length=100
    )
    editora = models.CharField(
        max_length=100
    )
    ano_publicacao = models.CharField(
        max_length=10
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
        max_length=10
    )
    cutter = models.CharField(
        max_length=20
    )
    paginas = models.CharField(
        max_length=10
    )
    foto_capa = models.CharField(
        max_length=100,
        blank=True
    )

    class Meta:
        db_table = 'livros'
        ordering = [
            'titulo',
            'autor_principal',
            'autores_secundarios'
        ]
