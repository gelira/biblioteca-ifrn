import os
import requests
from circulacao.celery import app

CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')
CATALOGO_QUEUE = os.getenv('CATALOGO_QUEUE')

def api_consulta_exemplar(codigo):
    return requests.get(CATALOGO_SERVICE_URL + '/exemplares/consulta/' + codigo)

def task_exemplares_devolvidos(codigos):
    app.send_task(
        'catalogoapp.tasks.exemplares_devolvidos',
        [codigos],
        queue=CATALOGO_QUEUE
    )

def task_exemplares_emprestados(codigos):
    app.send_task(
        'catalogoapp.tasks.exemplares_emprestados',
        [codigos],
        queue=CATALOGO_QUEUE
    )
