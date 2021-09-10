import os
from avaliacao.celery import app

CATALOGO_QUEUE = os.getenv('CATALOGO_QUEUE')

class CatalogoService:
    @classmethod
    def atualizar_nota(cls, livro_id, nota):
        app.send_task(
            'catalogo.atualizar_nota', 
            args=[livro_id, nota],
            ignore_task=True, 
            queue=CATALOGO_QUEUE
        )
