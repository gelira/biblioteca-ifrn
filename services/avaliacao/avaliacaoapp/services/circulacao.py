import os
from avaliacao.celery import app

CIRCULACAO_QUEUE = os.getenv('CIRCULACAO_QUEUE')

class CirculacaoService:
    @classmethod
    def get_emprestimo(cls, emprestimo_id, usuario_id):
        task = app.send_task(
            'circulacao.get_emprestimo', 
            args=[emprestimo_id, usuario_id], 
            queue=CIRCULACAO_QUEUE
        )
        return task.get()

    @classmethod
    def emprestimo_avaliado(cls, emprestimo_id):
        app.send_task(
            'circulacao.emprestimo_avaliado', 
            args=[emprestimo_id],
            ignore_task=True, 
            queue=CIRCULACAO_QUEUE
        )
