from __future__ import absolute_import, unicode_literals

from django.utils.timezone import localtime

from circulacaoapp.models import Emprestimo

def _emprestimo_avaliado(emprestimo_id):
    Emprestimo.objects.filter(_id=emprestimo_id).update(
        avaliado=True,
        updated=localtime()
    )
