from __future__ import absolute_import, unicode_literals

import os
import requests

CIRCULACAO_SERVICE_URL = os.getenv('CIRCULACAO_SERVICE_URL')

def _emprestimo_avaliado(usuario_id, emprestimo_id):
    r = requests.patch(
        CIRCULACAO_SERVICE_URL + '/emprestimos/' + emprestimo_id + '/avaliado', 
        headers={'X-Usuario-Id': usuario_id}
    )
    r.raise_for_status()
