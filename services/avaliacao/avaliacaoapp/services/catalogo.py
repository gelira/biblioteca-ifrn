import os
import requests

from .. import exceptions

from .base import datetime_name, save_clocked_task

AVALIACAO_USUARIO_ID = os.getenv('AVALIACAO_USUARIO_ID')

CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')
CATALOGO_TIMEOUT = int(os.getenv('CATALOGO_TIMEOUT'))

AVALIACAO_QUEUE = os.getenv('AVALIACAO_QUEUE')

class CatalogoService:
    url_buscar_livro = CATALOGO_SERVICE_URL + '/livros/'
    url_atualizar_nota = CATALOGO_SERVICE_URL + '/livros/atualizar-nota'

    task_atualizar_nota = 'avaliacao.atualizar_nota'

    @classmethod
    def atualizar_nota(cls, livro_id, nota):
        cls.dispatch({
            'url': cls.url_atualizar_nota,
            'method': 'PATCH',
            'headers': {
                'X-Usuario-Id': AVALIACAO_USUARIO_ID,
            },
            'json': {
                'livro_id': livro_id,
                'nota': nota
            }
        })

    @classmethod
    def call_atualizar_nota(cls, livro_id, nota):
        try:
            cls.atualizar_nota(livro_id, nota)
        
        except:
            name = datetime_name(cls.task_atualizar_nota)
            save_clocked_task(
                name=name,
                task=cls.task_atualizar_nota,
                args=[livro_id, nota],
                queue=AVALIACAO_QUEUE
            )

    @classmethod
    def busca_livro(cls, livro_id):
        response = cls.dispatch({
            'url': cls.url_buscar_livro + livro_id,
            'method': 'GET',
            'params': {
                'sem_exemplares': True
            }
        })

        return response.json()

    @classmethod
    def dispatch(cls, options):
        method = options.pop('method')
        url = options.pop('url')
        options['timeout'] = CATALOGO_TIMEOUT
        
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

