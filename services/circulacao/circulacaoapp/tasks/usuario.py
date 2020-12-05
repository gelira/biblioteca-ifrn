from __future__ import absolute_import, unicode_literals

import os
import requests

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')

def _usuarios_suspensos(usuario_id, usuarios):
    lista = []
    for key in usuarios.keys():
        lista.append({
            'usuario_id': key,
            'dias': usuarios[key]
        })

    r = requests.put(
        AUTENTICACAO_SERVICE_URL + '/suspensoes', 
        headers={'X-Usuario-Id': usuario_id},
        json={'usuarios': lista}
    )
    r.raise_for_status()

def _usuarios_abono(usuario_id, usuarios):
    lista = []
    for key in usuarios.keys():
        lista.append({
            'usuario_id': key,
            'dias': usuarios[key]
        })

    r = requests.put(
        AUTENTICACAO_SERVICE_URL + '/abonos', 
        headers={'X-Usuario-Id': usuario_id},
        json={'usuarios': lista}
    )
    r.raise_for_status()