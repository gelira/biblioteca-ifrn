from __future__ import absolute_import, unicode_literals

import os
from django.core.mail import send_mail
from django.template.loader import render_to_string

EMAIL_SENDER = os.getenv('EMAIL_SENDER')

def compor_e_enviar_email(contexto, emails, assunto, template_html, template_txt):
    msg_html = render_to_string(template_html, contexto)
    msg_plain = render_to_string(template_txt, contexto)
    send_mail(
        assunto,
        msg_plain,
        EMAIL_SENDER,
        emails,
        html_message=msg_html
    )

def comprovante_emprestimo(contexto, emails):
    compor_e_enviar_email(
        contexto, 
        emails, 
        'Comprovante de Empréstimo', 
        'comprovante_emprestimo.html', 
        'comprovante_emprestimo.txt'
    )

def comprovante_devolucao(contexto, emails):
    compor_e_enviar_email(
        contexto, 
        emails, 
        'Comprovante de Devolução', 
        'comprovante_devolucao.html', 
        'comprovante_devolucao.txt'
    )

def reserva_disponivel(contexto, emails):
    compor_e_enviar_email(
        contexto, 
        emails, 
        'Reserva Disponível', 
        'reserva_disponivel.html', 
        'reserva_disponivel.txt'
    )
