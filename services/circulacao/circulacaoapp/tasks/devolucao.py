from __future__ import absolute_import, unicode_literals

import os
import requests
from circulacao.celery import app

USUARIO_SISTEMA_ID = os.getenv('USUARIO_SISTEMA_ID')
NOTIFICACAO_QUEUE = os.getenv('NOTIFICACAO_QUEUE')
CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')
AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')

def _enviar_comprovantes_devolucao(comprovantes):
    usuarios = {}
    livros = {}

    for comprovante in comprovantes:
        usuario_id = comprovante['usuario_id']
        livro_id = comprovante['livro_id']

        if usuario_id not in usuarios:
            r = requests.get(
                AUTENTICACAO_SERVICE_URL + '/consulta', 
                headers={ 'X-Usuario-Id': USUARIO_SISTEMA_ID },
                params={ 'id': usuario_id }
            )
            r.raise_for_status()
            usuarios[usuario_id] = r.json()

        if livro_id not in livros:
            r = requests.get(
                CATALOGO_SERVICE_URL + '/livros/' + livro_id,
                params={ 'min': '1' }
            )
            r.raise_for_status()
            livros[livro_id] = r.json()

        usuario = usuarios[usuario_id]
        livro = livros[livro_id]

        emails = [usuario['email_institucional']]
        if usuario['email_pessoal']:
            emails.append(usuario['email_pessoal'])

        comprovante.update({
            'nome_usuario': usuario['nome'],
            'titulo': livro['titulo']
        })

        app.send_task(
            'notificacaoapp.tasks.comprovante_devolucao', 
            [comprovante, emails], 
            queue=NOTIFICACAO_QUEUE
        )
