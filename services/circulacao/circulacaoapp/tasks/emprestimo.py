from __future__ import absolute_import, unicode_literals

import os
import requests

CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')

def _marcar_exemplares_emprestados(usuario_id, codigos):
    r = requests.put(
        CATALOGO_SERVICE_URL + '/exemplares/emprestados', 
        headers={'X-Usuario-Id': usuario_id},
        json={'codigos': codigos}
    )
    r.raise_for_status()


def _marcar_exemplares_devolvidos(usuario_id, codigos):
    r = requests.put(
        CATALOGO_SERVICE_URL + '/exemplares/devolvidos', 
        headers={'X-Usuario-Id': usuario_id},
        json={'codigos': codigos}
    )
    r.raise_for_status()
