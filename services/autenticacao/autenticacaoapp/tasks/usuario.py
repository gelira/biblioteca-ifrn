from __future__ import absolute_import, unicode_literals

import os
import requests
from django.utils import timezone
from django.db import transaction

from autenticacaoapp.models import Usuario

def _usuarios_suspensos(usuarios):
    hoje = timezone.localdate()
    
    with transaction.atomic():
        for u in usuarios:
            dias_suspensao = int(u['dias'])
            if dias_suspensao <= 0:
                continue

            usuario = Usuario.objects.filter(_id=u['usuario_id']).first()
            if usuario is None:
                continue

            if usuario.suspensao is None or usuario.suspensao < hoje:
                usuario.suspensao = hoje - timezone.timedelta(days=1)

            usuario.suspensao += timezone.timedelta(days=dias_suspensao)
            usuario.save()

def _usuarios_abono(usuarios):
    hoje = timezone.localdate()

    with transaction.atomic():
        for u in usuarios:
            dias_suspensao = int(u['dias'])
            if dias_suspensao <= 0:
                continue

            usuario = Usuario.objects.filter(_id=u['usuario_id']).first()
            if usuario is None:
                continue

            if usuario.suspensao is None:
                continue
            
            if usuario.suspensao >= hoje:
                usuario.suspensao -= timezone.timedelta(days=int(u['dias']))
                usuario.save()
