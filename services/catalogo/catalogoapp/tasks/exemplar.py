from __future__ import absolute_import, unicode_literals

import os
import requests
from django.utils.timezone import localtime

from catalogoapp.models import Exemplar

def disponibilidade_exemplares(codigos, disponivel):
    Exemplar.objects.filter(codigo__in=codigos).update(
        disponivel=disponivel,
        updated=localtime()
    )

def _exemplares_emprestados(codigos):
    disponibilidade_exemplares(codigos, False)

def _exemplares_devolvidos(codigos):
    disponibilidade_exemplares(codigos, True)
