import os
import requests
from circulacao.celery import app

AUTENTICACAO_QUEUE = os.getenv('AUTENTICACAO_QUEUE')
AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')
USUARIO_SISTEMA_ID = os.getenv('USUARIO_SISTEMA_ID')

def api_autenticar_usuario(matricula, senha):
    return requests.post(
        AUTENTICACAO_SERVICE_URL + '/token', 
        json={
            'username': matricula, 
            'password': senha
        }
    )

def api_consulta_usuario(usuario_id):
    return requests.get(
        AUTENTICACAO_SERVICE_URL + '/consulta', 
        headers={ 
            'X-Usuario-Id': USUARIO_SISTEMA_ID 
        },
        params={ 
            'id': usuario_id 
        }
    )

def api_informacoes_usuario(token):
    return requests.get(
        AUTENTICACAO_SERVICE_URL + '/informacoes', 
        headers={
            'Authorization': 'JWT {}'.format(token)
        }
    )

def task_usuarios_abono(usuarios):
    lista = []
    for key in usuarios.keys():
        lista.append({
            'usuario_id': key,
            'dias': usuarios[key]
        })

    app.send_task(
        'autenticacaoapp.tasks.usuarios_abono',
        [lista],
        queue=AUTENTICACAO_QUEUE
    )

def task_usuarios_suspensos(usuarios):
    lista = []
    for key in usuarios.keys():
        lista.append({
            'usuario_id': key,
            'dias': usuarios[key]
        })

    app.send_task(
        'autenticacaoapp.tasks.usuarios_suspensos',
        [lista],
        queue=AUTENTICACAO_QUEUE
    )
