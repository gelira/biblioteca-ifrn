import os
import requests

CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')

def api_get_livro(livro_id, params = {}):
    return requests.get(
        CATALOGO_SERVICE_URL + '/livros/' + livro_id,
        params=params
    )
