from __future__ import absolute_import, unicode_literals

import os
import requests
from celery import shared_task

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')
CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')

@shared_task(bind=True)
def marcar_exemplares_emprestados(self, usuario_id, codigos):
    try:
        r = requests.put(
            CATALOGO_SERVICE_URL + '/exemplares/emprestados', 
            headers={'X-Usuario-Id': usuario_id},
            json={'codigos': codigos}
        )
        r.raise_for_status()
    except Exception as e:
        raise self.retry(exc=e, countdown=10)

@shared_task(bind=True)
def usuarios_suspensos(self, usuario_id, usuarios):
    try:
        lista = []
        for key in usuarios.keys():
            lista.append({
                'usuario_id': key,
                'dias_suspensao': usuarios[key]
            })

        r = requests.post(
            AUTENTICACAO_SERVICE_URL + '/suspensoes', 
            headers={'X-Usuario-Id': usuario_id},
            json={'usuarios': lista}
        )
        r.raise_for_status()
    except Exception as e:
        raise self.retry(exc=e, countdown=10)
