import os
from django.core.mail import send_mail
from django.template.loader import render_to_string

EMAIL_SENDER = os.getenv('EMAIL_SENDER')

class EmailService:
    @classmethod
    def comprovante_emprestimo(cls, contexto, emails):
        cls.compor_e_enviar_email(
            contexto, 
            emails, 
            'Comprovante de Empréstimo', 
            'comprovante_emprestimo.html', 
            'comprovante_emprestimo.txt'
        )

    @classmethod
    def comprovante_devolucao(cls, contexto, emails):
        cls.compor_e_enviar_email(
            contexto, 
            emails, 
            'Comprovante de Devolução', 
            'comprovante_devolucao.html', 
            'comprovante_devolucao.txt'
        )

    @classmethod
    def reserva_disponivel(cls, contexto, emails):
        cls.compor_e_enviar_email(
            contexto, 
            emails, 
            'Reserva Disponível', 
            'reserva_disponivel.html', 
            'reserva_disponivel.txt'
        )

    @classmethod
    def reserva_cancelada(cls, contexto, emails):
        cls.compor_e_enviar_email(
            contexto, 
            emails, 
            'Reserva Cancelada', 
            'reserva_cancelada.html', 
            'reserva_cancelada.txt'
        )

    @classmethod
    def avaliacao_moderada(cls, contexto, emails):
        cls.compor_e_enviar_email(
            contexto, 
            emails, 
            'Aviso de Moderação', 
            'avaliacao_moderada.html', 
            'avaliacao_moderada.txt'
        )

    @classmethod
    def avaliacao_publicada(cls, contexto, emails):
        cls.compor_e_enviar_email(
            contexto, 
            emails, 
            'Avaliação Publicada', 
            'avaliacao_publicada.html', 
            'avaliacao_publicada.txt'
        )

    @classmethod
    def comprovante_renovacao(cls, contexto, emails):
        cls.compor_e_enviar_email(
            contexto, 
            emails, 
            'Comprovante de Renovação', 
            'comprovante_renovacao.html', 
            'comprovante_renovacao.txt'
        )

    @classmethod
    def comprovante_reserva(cls, contexto, emails):
        cls.compor_e_enviar_email(
            contexto, 
            emails, 
            'Comprovante de Reserva', 
            'comprovante_reserva.html', 
            'comprovante_reserva.txt'
        )

    @classmethod
    def comprovante_reserva_cancelada(cls, contexto, emails):
        cls.compor_e_enviar_email(
            contexto, 
            emails, 
            'Comprovante de Cancelamento de Reserva', 
            'comprovante_reserva_cancelada.html', 
            'comprovante_reserva_cancelada.txt'
        )

    @classmethod
    def alerta_emprestimo_vencendo(cls, contexto, emails):
        cls.compor_e_enviar_email(
            contexto, 
            emails, 
            'Empréstimo próximo do vencimento', 
            'alerta_emprestimo_vencendo.html', 
            'alerta_emprestimo_vencendo.txt'
        )

    @classmethod
    def alerta_emprestimo_atrasado(cls, contexto, emails):
        cls.compor_e_enviar_email(
            contexto, 
            emails, 
            'Empréstimo Atrasado', 
            'alerta_emprestimo_atrasado.html', 
            'alerta_emprestimo_atrasado.txt'
        )

    @classmethod
    def alerta_sugestao_listada(cls, contexto, emails):
        cls.compor_e_enviar_email(
            contexto, 
            emails, 
            'Sugestão Listada', 
            'sugestao_listada_alerta.html', 
            'sugestao_listada_alerta.txt'
        )

    @classmethod
    def compor_e_enviar_email(cls, contexto, emails, assunto, template_html, template_txt):
        msg_html = render_to_string(template_html, contexto)
        msg_plain = render_to_string(template_txt, contexto)
        send_mail(
            assunto,
            msg_plain,
            EMAIL_SENDER,
            emails,
            html_message=msg_html
        )
