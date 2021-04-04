import os
import requests
from avaliacao.celery import app

CIRCULACAO_SERVICE_URL = os.getenv('CIRCULACAO_SERVICE_URL')
CIRCULACAO_QUEUE = os.getenv('CIRCULACAO_QUEUE')

def api_get_emprestimo(emprestimo_id, usuario_id):
    return requests.get(
        CIRCULACAO_SERVICE_URL + '/emprestimos/' + emprestimo_id, 
        headers={
            'X-Usuario-Id': usuario_id
        }
    )

def task_emprestimo_avaliado(emprestimo_id):
    app.send_task(
        'circulacaoapp.taks.emprestimo_avaliado',
        [emprestimo_id],
        queue=CIRCULACAO_QUEUE
    )
