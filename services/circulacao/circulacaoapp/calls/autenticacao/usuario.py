import os
import requests

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')
USUARIO_SISTEMA_ID = os.getenv('USUARIO_SISTEMA_ID')

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
