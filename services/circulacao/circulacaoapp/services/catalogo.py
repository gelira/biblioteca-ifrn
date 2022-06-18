import os
import requests

from .. import exceptions
from .base import save_clocked_task, datetime_name

CIRCULACAO_USUARIO_ID = os.getenv('CIRCULACAO_USUARIO_ID')

CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')
CATALOGO_TIMEOUT = int(os.getenv('CATALOGO_TIMEOUT'))

CIRCULACAO_QUEUE = os.getenv('CIRCULACAO_QUEUE')

class CatalogoService:
    url_consulta_exemplar = CATALOGO_SERVICE_URL + '/exemplares/consulta'
    url_exemplares_emprestados = CATALOGO_SERVICE_URL + '/exemplares/emprestados'
    url_exemplares_devolvidos = CATALOGO_SERVICE_URL + '/exemplares/devolvidos'
    url_buscar_livro = CATALOGO_SERVICE_URL + '/livros'

    task_exemplares_emprestados = 'circulacao.exemplares_emprestados'
    task_exemplares_devolvidos = 'circulacao.exemplares_devolvidos'

    @classmethod
    def consulta_codigo_exemplar(cls, codigo):
        response = cls.dispatch({
            'url': f'{cls.url_consulta_exemplar}/{codigo}',
            'method': 'GET'
        })

        return response.json()

    @classmethod
    def exemplares_emprestados(cls, codigos):
        cls.dispatch({
            'url': cls.url_exemplares_emprestados,
            'method': 'PATCH',
            'headers': {
                'X-Usuario-Id': CIRCULACAO_USUARIO_ID,
            },
            'json': {
                'codigos': codigos
            }
        })

    @classmethod
    def call_exemplares_emprestados(cls, codigos):
        try:
            cls.exemplares_emprestados(codigos)
        
        except:
            name = datetime_name(cls.task_exemplares_emprestados)
            save_clocked_task(
                name=name,
                task=cls.task_exemplares_emprestados,
                args=[codigos],
                queue=CIRCULACAO_QUEUE
            )

    @classmethod
    def exemplares_devolvidos(cls, codigos):
        cls.dispatch({
            'url': cls.url_exemplares_devolvidos,
            'method': 'PATCH',
            'headers': {
                'X-Usuario-Id': CIRCULACAO_USUARIO_ID,
            },
            'json': {
                'codigos': codigos
            }
        })
    
    @classmethod
    def call_exemplares_devolvidos(cls, codigos):
        try:
            cls.exemplares_devolvidos(codigos)
        
        except:
            name = datetime_name(cls.task_exemplares_devolvidos)
            save_clocked_task(
                name=name,
                task=cls.task_exemplares_devolvidos,
                args=[codigos],
                queue=CIRCULACAO_QUEUE
            )

    @classmethod
    def busca_livro(cls, livro_id, **params):
        response = cls.dispatch({
            'url': f'{cls.url_buscar_livro}/{livro_id}',
            'method': 'GET',
            'params': params
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
