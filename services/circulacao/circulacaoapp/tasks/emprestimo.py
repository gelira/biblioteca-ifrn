from __future__ import absolute_import, unicode_literals

import os
import requests

USUARIO_SISTEMA_ID = os.getenv('USUARIO_SISTEMA_ID')
CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')

def _marcar_exemplares_emprestados(codigos):
    r = requests.put(
        CATALOGO_SERVICE_URL + '/exemplares/emprestados', 
        headers={ 'X-Usuario-Id': USUARIO_SISTEMA_ID },
        json={ 'codigos': codigos }
    )
    r.raise_for_status()

def _marcar_exemplares_devolvidos(codigos):
    r = requests.put(
        CATALOGO_SERVICE_URL + '/exemplares/devolvidos', 
        headers={ 'X-Usuario-Id': USUARIO_SISTEMA_ID },
        json={ 'codigos': codigos }
    )
    r.raise_for_status()
