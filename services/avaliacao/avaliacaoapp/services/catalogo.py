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

    @classmethod
    def busca_livro(cls, livro_id):
        task = app.send_task(
            'catalogo.busca_livro', 
            args=[livro_id],
            kwargs={ 'min': True }, 
            queue=CATALOGO_QUEUE
        )
        return task.get(disable_sync_subtasks=False)
