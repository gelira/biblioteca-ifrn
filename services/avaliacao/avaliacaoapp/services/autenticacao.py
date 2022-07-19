import os
import requests

from .. import exceptions

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')
AUTENTICACAO_TIMEOUT = int(os.getenv('AUTENTICACAO_TIMEOUT'))

class AutenticacaoService:
    url_informacoes_usuario = AUTENTICACAO_SERVICE_URL + '/informacoes'

    @classmethod
    def informacoes_usuario(cls, usuario_id, save_cache=False):
        options = { 
            'method': 'GET', 
            'url': cls.url_informacoes_usuario,
            'headers': { 
                'X-Usuario-Id': usuario_id, 
            },
        }

        if save_cache:
            options['params'] = {
                'save_cache': True
            }

        response = cls.dispatch(options)

        return response.json()

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
