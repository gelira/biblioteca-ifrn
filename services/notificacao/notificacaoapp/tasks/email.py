from __future__ import absolute_import, unicode_literals

import os
from django.core.mail import send_mail
from django.template.loader import render_to_string

EMAIL_SENDER = os.getenv('EMAIL_SENDER')

def comprovante_emprestimo(contexto, emails):
    msg_plain = render_to_string('comprovante_emprestimo.txt', contexto)
    msg_html = render_to_string('comprovante_emprestimo.html', contexto)
    send_mail(
        'Comprovante de Empréstimo',
        msg_plain,
        EMAIL_SENDER,
        emails,
        html_message=msg_html
    )
