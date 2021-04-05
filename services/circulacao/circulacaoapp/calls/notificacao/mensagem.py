import os
from circulacao.celery import app

NOTIFICACAO_QUEUE = os.getenv('NOTIFICACAO_QUEUE')

def task_comprovante_emprestimo(contexto_email, emails):
    app.send_task(
        'notificacaoapp.tasks.comprovante_emprestimo', 
        [contexto_email, emails], 
        queue=NOTIFICACAO_QUEUE
    )

def task_comprovante_devolucao(contexto_email, emails):
    app.send_task(
        'notificacaoapp.tasks.comprovante_devolucao', 
        [contexto_email, emails], 
        queue=NOTIFICACAO_QUEUE
    )
