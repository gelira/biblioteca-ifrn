import uuid
from django.db import models

from .timestamped import TimestampedModel

# não apagar essa função
def nome_arquivo(instance, filename):
    nome = str(instance._id)
    sub1 = nome[0]
    sub2 = nome[1]
    return '{}/{}/{}'.format(sub1, sub2, nome)

class Livro(TimestampedModel):
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

    def get_versao_atual(self):
        if not hasattr(self, 'foto_capa'):
            return ''
        
        versao = self.foto_capa.versoes.filter(atual=True).first()
        if not versao:
            return ''

        return versao.version_id

    def get_foto_url(self):
        if not hasattr(self, 'foto_capa'):
            return ''

        f = self.foto_capa

        url = f'https://{f.bucket}.s3.{f.region}.amazonaws.com/{f.key}'
        
        version_id = self.get_versao_atual()
        if version_id:
            url = f'{url}?versionId={version_id}'
        
        return url

    class Meta:
        db_table = 'livros'
        ordering = [
            'titulo',
            'autor_principal',
            'autores_secundarios'
        ]
