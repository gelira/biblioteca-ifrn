import os
import requests

from .. import exceptions

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')

AUTENTICACAO_TIMEOUT = int(os.getenv('AUTENTICACAO_TIMEOUT'))

AUTENTICACAO_TOKEN = (
    AUTENTICACAO_SERVICE_URL + os.getenv('AUTENTICACAO_TOKEN'))

AUTENTICACAO_INFORMACOES_USUARIO = (
    AUTENTICACAO_SERVICE_URL + os.getenv('AUTENTICACAO_INFORMACOES_USUARIO'))

AUTENTICACAO_CONSULTA_USUARIO = (
    AUTENTICACAO_SERVICE_URL + os.getenv('AUTENTICACAO_CONSULTA_USUARIO'))

AUTENTICACAO_SUSPENSOES = (
    AUTENTICACAO_SERVICE_URL + os.getenv('AUTENTICACAO_SUSPENSOES'))

AUTENTICACAO_ABONO_SUSPENSOES = (
    AUTENTICACAO_SERVICE_URL + os.getenv('AUTENTICACAO_ABONO_SUSPENSOES'))

AUTENTICACAO_QUEUE = os.getenv('AUTENTICACAO_QUEUE')

class AutenticacaoService:
    @classmethod
    def autenticar_usuario(cls, matricula, senha):
        data_token = cls.login_suap(matricula, senha)
        return cls.informacoes_usuario(token=data_token['token'])

    @classmethod
    def login_suap(cls, username, password):
        return cls.dispatch({
            'method': 'POST',
            'url': AUTENTICACAO_TOKEN,
            'json': {
                'username': username,
                'password': password
            }
        })

    @classmethod
    def informacoes_usuario(cls, usuario_id=None, token=None):
        if not usuario_id and not token:
            raise Exception('Uma das opções deve ser definida: usuario_id ou token')
        
        options = { 
            'method': 'GET' 
        }

        if usuario_id:
            options.update({
                'url': AUTENTICACAO_CONSULTA_USUARIO,
                'params': {
                    'id': usuario_id
                }
            })

        else:
            options.update({
                'url': AUTENTICACAO_INFORMACOES_USUARIO,
                'headers': {
                    'Authorization': f'JWT {token}'
                }
            })

        return cls.dispatch(options)

    @classmethod
    def suspensoes(cls, suspensoes):
        return cls.dispatch({
            'method': 'POST',
            'url': AUTENTICACAO_SUSPENSOES,
            'json': suspensoes
        })
    
    @classmethod
    def abono_suspensoes(cls, suspensoes):
        return cls.dispatch({
            'method': 'POST',
            'url': AUTENTICACAO_ABONO_SUSPENSOES,
            'json': suspensoes
        })

    @classmethod
    def dispatch(self, options):
        method = options.pop('method')
        url = options.pop('url')
        options['timeout'] = AUTENTICACAO_TIMEOUT
        
        try:
            response = requests.request(method, url, **options)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError:
            raise exceptions.ServiceUnauthorized
        
        except requests.exceptions.ConnectTimeout:
            raise exceptions.ServiceTimeOut
        
        except requests.exceptions.ConnectionError:
            raise exceptions.ServiceUnavailable
