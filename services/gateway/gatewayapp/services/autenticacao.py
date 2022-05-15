import os
import requests

from .. import exceptions

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')

AUTENTICACAO_TIMEOUT = int(os.getenv('AUTENTICACAO_TIMEOUT'))

AUTENTICACAO_VERIFICAR_TOKEN = (
    AUTENTICACAO_SERVICE_URL + os.getenv('AUTENTICACAO_VERIFICAR_TOKEN'))

AUTENTICACAO_INFORMACOES_USUARIO = (
    AUTENTICACAO_SERVICE_URL + os.getenv('AUTENTICACAO_INFORMACOES_USUARIO'))

class AutenticacaoService:
    @classmethod
    def verificar_token(cls, token):
        return cls.dispatch({
            'method': 'GET',
            'url': AUTENTICACAO_VERIFICAR_TOKEN,
            'headers': {
                'Authorization': f'JWT {token}'
            }
        })

    @classmethod
    def informacoes_usuario(cls, token):
        return cls.dispatch({
            'method': 'GET',
            'url': AUTENTICACAO_INFORMACOES_USUARIO,
            'headers': {
                'Authorization': f'JWT {token}'
            }
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
