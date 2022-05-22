import os
import requests

from .. import exceptions

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')
AUTENTICACAO_TIMEOUT = int(os.getenv('AUTENTICACAO_TIMEOUT'))

class AutenticacaoService:
    url_token = AUTENTICACAO_SERVICE_URL + '/token'
    url_informacoes_usuario = AUTENTICACAO_SERVICE_URL + '/informacoes'
    url_consulta_usuario = AUTENTICACAO_SERVICE_URL + '/consulta'
    url_suspensoes = AUTENTICACAO_SERVICE_URL + '/suspensoes'
    url_abono_suspensoes = AUTENTICACAO_SERVICE_URL + '/abono-suspensoes'

    @classmethod
    def autenticar_usuario(cls, matricula, senha):
        data_token = cls.login_suap(matricula, senha)
        return cls.informacoes_usuario(token=data_token['token'])

    @classmethod
    def login_suap(cls, username, password):
        response = cls.dispatch({
            'method': 'POST',
            'url': cls.url_token,
            'json': {
                'username': username,
                'password': password
            }
        })

        return response.json()

    @classmethod
    def informacoes_usuario(cls, usuario_id=None, token=None):
        if not usuario_id and not token:
            raise Exception('Uma das opções deve ser definida: usuario_id ou token')
        
        options = { 
            'method': 'GET' 
        }

        if usuario_id:
            options.update({
                'url': cls.url_consulta_usuario,
                'params': {
                    'id': usuario_id
                }
            })

        else:
            options.update({
                'url': cls.url_informacoes_usuario,
                'headers': {
                    'Authorization': f'JWT {token}'
                }
            })

        response = cls.dispatch(options)

        return response.json()

    @classmethod
    def suspensoes(cls, suspensoes):
        cls.dispatch({
            'method': 'POST',
            'url': cls.url_suspensoes,
            'json': suspensoes
        })
    
    @classmethod
    def abono_suspensoes(cls, suspensoes):
        cls.dispatch({
            'method': 'POST',
            'url': cls.url_abono_suspensoes,
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
            return response

        except requests.exceptions.HTTPError:
            raise exceptions.ServiceUnauthorized
        
        except requests.exceptions.ConnectTimeout:
            raise exceptions.ServiceTimeOut
        
        except requests.exceptions.ConnectionError:
            raise exceptions.ServiceUnavailable
