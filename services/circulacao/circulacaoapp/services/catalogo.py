import os
from circulacao.celery import app

CATALOGO_QUEUE = os.getenv('CATALOGO_QUEUE')

class CatalogoService:
    @classmethod
    def consulta_codigo_exemplar(cls, codigo):
        task = app.send_task(
            'catalogo.consulta_codigo_exemplar', 
            args=[codigo], 
            queue=CATALOGO_QUEUE
        )
        return task.get()

    @classmethod
    def exemplares_emprestados(cls, codigo):
        app.send_task(
            'catalogo.exemplares_emprestados', 
            args=[codigo],
            ignore_task=True, 
            queue=CATALOGO_QUEUE
        )

    @classmethod
    def exemplares_devolvidos(cls, codigo):
        app.send_task(
            'catalogo.exemplares_devolvidos', 
            args=[codigo], 
            ignore_task=True,
            queue=CATALOGO_QUEUE
        )

    @classmethod
    def busca_livro(cls, livro_id, **kwargs):
        task = app.send_task(
            'catalogo.busca_livro', 
            args=[livro_id],
            kwargs=kwargs, 
            queue=CATALOGO_QUEUE
        )
        return task.get()
