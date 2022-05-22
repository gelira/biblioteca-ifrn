import os
import requests

from .. import exceptions

CIRCULACAO_SERVICE_URL = os.getenv('CIRCULACAO_SERVICE_URL')
CIRCULACAO_TIMEOUT = int(os.getenv('CIRCULACAO_TIMEOUT'))

class CirculacaoService:
    url_emprestimos = CIRCULACAO_SERVICE_URL + '/emprestimos'

    @classmethod
    def get_emprestimo(cls, emprestimo_id, usuario_id):
        try:
            response = cls.dispatch({
                'url': f'{cls.url_emprestimos}/{emprestimo_id}',
                'method': 'GET',
                'headers': {
                    'X-Usuario-Id': usuario_id
                }
            })

            return response.json()

        except:
            return None

    @classmethod
    def emprestimo_avaliado(cls, emprestimo_id):
        cls.dispatch({
            'url': f'{cls.url_emprestimos}/{emprestimo_id}/avaliado',
            'method': 'PATCH'
        })

    @classmethod
    def dispatch(cls, options):
        method = options.pop('method')
        url = options.pop('url')
        options['timeout'] = CIRCULACAO_TIMEOUT
        
        try:
            response = requests.request(method, url, **options)
            response.raise_for_status()
            return response

        except requests.exceptions.HTTPError:
            raise exceptions.ServiceBadRequest
        
        except requests.exceptions.ConnectTimeout:
            raise exceptions.ServiceTimeOut
        
        except requests.exceptions.ConnectionError:
            raise exceptions.ServiceUnavailable
