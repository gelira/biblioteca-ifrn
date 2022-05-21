import os
import requests

from .. import exceptions

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')
AUTENTICACAO_TIMEOUT = int(os.getenv('AUTENTICACAO_TIMEOUT'))

class AutenticacaoService:
    url_verificar_token = AUTENTICACAO_SERVICE_URL + '/verificar'
    url_informacoes_usuario = AUTENTICACAO_SERVICE_URL + '/informacoes'

    @classmethod
    def verificar_token(cls, token):
        return cls.dispatch({
            'method': 'GET',
            'url': cls.url_verificar_token,
            'headers': {
                'Authorization': f'JWT {token}'
            }
        })

    @classmethod
    def informacoes_usuario(cls, token):
        return cls.dispatch({
            'method': 'GET',
            'url': cls.url_informacoes_usuario,
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
