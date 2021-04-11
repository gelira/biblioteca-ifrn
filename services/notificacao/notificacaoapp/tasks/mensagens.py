from __future__ import absolute_import, unicode_literals

from notificacaoapp.tasks import email

def _comprovante_emprestimo(contexto, emails):
    email.comprovante_emprestimo(contexto, emails)

def _comprovante_devolucao(contexto, emails):
    email.comprovante_devolucao(contexto, emails)

def _reserva_disponivel(contexto, emails):
    email.reserva_disponivel(contexto, emails)

def _reserva_cancelada(contexto, emails):
    email.reserva_cancelada(contexto, emails)
