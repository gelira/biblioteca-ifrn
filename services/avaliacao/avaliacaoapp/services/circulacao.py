import os
import requests

from .. import exceptions

from .base import datetime_name, save_clocked_task

AVALIACAO_USUARIO_ID = os.getenv('AVALIACAO_USUARIO_ID')

CIRCULACAO_SERVICE_URL = os.getenv('CIRCULACAO_SERVICE_URL')
CIRCULACAO_TIMEOUT = int(os.getenv('CIRCULACAO_TIMEOUT'))

AVALIACAO_QUEUE = os.getenv('AVALIACAO_QUEUE')

class CirculacaoService:
    url_emprestimos = CIRCULACAO_SERVICE_URL + '/emprestimos'

    task_emprestimo_avaliado = 'avaliacao.emprestimo_avaliado'

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
            'method': 'PATCH',
            'headers': {
                'X-Usuario-Id': AVALIACAO_USUARIO_ID,
            },
        })

    @classmethod
    def call_emprestimo_avaliado(cls, emprestimo_id):
        try:
            cls.emprestimo_avaliado(emprestimo_id)
        
        except:
            name = datetime_name(cls.task_emprestimo_avaliado)
            save_clocked_task(
                name=name,
                task=cls.task_emprestimo_avaliado,
                args=[emprestimo_id],
                queue=AVALIACAO_QUEUE
            )

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
