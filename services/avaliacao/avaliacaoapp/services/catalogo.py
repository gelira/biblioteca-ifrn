import os
import requests

from .. import exceptions

CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')
CATALOGO_TIMEOUT = int(os.getenv('CATALOGO_TIMEOUT'))

class CatalogoService:
    url_buscar_livro = CATALOGO_SERVICE_URL + '/livros/'
    url_atualizar_nota = CATALOGO_SERVICE_URL + '/livros/atualizar-nota'

    @classmethod
    def atualizar_nota(cls, livro_id, nota):
        return cls.dispatch({
            'url': cls.url_atualizar_nota,
            'method': 'PATCH',
            'json': {
                'livro_id': livro_id,
                'nota': nota
            }
        })

    @classmethod
    def busca_livro(cls, livro_id):
        return cls.dispatch({
            'url': cls.url_buscar_livro + livro_id,
            'method': 'GET',
            'params': {
                'sem_exemplares': True
            }
        })

    @classmethod
    def dispatch(cls, options):
        method = options.pop('method')
        url = options.pop('url')
        options['timeout'] = CATALOGO_TIMEOUT
        
        try:
            response = requests.request(method, url, **options)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError:
            raise exceptions.ServiceBadRequest
        
        except requests.exceptions.ConnectTimeout:
            raise exceptions.ServiceTimeOut
        
        except requests.exceptions.ConnectionError:
            raise exceptions.ServiceUnavailable

