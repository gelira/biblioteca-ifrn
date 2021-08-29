import os
import io
import base64
from django.db import transaction
from catalogo.celery import app

from ..models import (
    Livro,
    FotoCapa,
    VersaoFotoCapa
)
from ..cliente_aws import get_bucket

CATALOGO_QUEUE = os.getenv('PROJECT_NAME')

class LivroService:
    @classmethod
    def busca_livro(cls, livro_id, **kwargs):
        livro = Livro.objects.filter(_id=livro_id).first()

        if not livro:
            raise Exception({
                'error': {
                    'detail': 'Livro não encontrado'
                },
                'status': 404
            })

        serializer_class = LivroSerializer if kwargs.get('min') \
            else LivroRetrieveSerializer
        
        ser = serializer_class(livro)
        return ser.data

    @classmethod
    def upload_foto_capa(cls, livro_id, livro_pk, foto_base64):
        with transaction.atomic():
            foto = FotoCapa.objects.filter(livro_id=livro_pk).first()
            
            if not foto:
                foto = FotoCapa.objects.create(
                    livro_id=livro_pk,
                    region=os.getenv('AWS_REGION'),
                    bucket=os.getenv('AWS_BUCKET'),
                    key=livro_id,
                )

            foto_bytes = base64.b64decode(foto_base64)
            foto_bytesio = io.BytesIO(foto_bytes)

            bucket = get_bucket()
            obj = bucket.Object(foto.key)
            obj.upload_fileobj(foto_bytesio, ExtraArgs={ 'ACL': 'public-read' })
            
            VersaoFotoCapa.objects.filter(foto_capa=foto, atual=True).update(atual=False)
            VersaoFotoCapa.objects.create(
                foto_capa=foto,
                version_id=obj.version_id,
                atual=True
            )

    @classmethod
    def task_upload_foto_capa(cls, livro_id, livro_pk, foto_base64):
        app.send_task(
            'catalogo.upload_foto_capa',
            args=[livro_id, livro_pk, foto_base64],
            ignore_task=True, 
            queue=CATALOGO_QUEUE
        )
