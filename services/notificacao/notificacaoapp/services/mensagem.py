from ..models import Contato

from .email import EmailService

class MensagemService:
    @classmethod
    def get_contato(cls, usuario_id):
        return Contato.objects.filter(usuario_id=usuario_id).first()

    @classmethod
    def get_emails_contato(cls, contato):
        emails = [contato.email_institucional]
        
        if contato.email_pessoal:
            emails.append(contato.email_pessoal)
        
        return emails

    @classmethod
    def load_info_usuario(cls, contato, contexto):
        contexto['nome_usuario'] = contato.nome
        return contexto

    @classmethod
    def load_info_atendente(cls, contato, contexto):
        contexto['nome_atendente'] = contato.nome
        contexto['matricula_atendente'] = contato.matricula
        return contexto

        EmailService.comprovante_emprestimo(contexto, emails)

    @classmethod
    def comprovante_devolucao(cls, contexto, emails):
        EmailService.comprovante_devolucao(contexto, emails)

    @classmethod
    def reserva_disponivel(cls, contexto, emails):
        EmailService.reserva_disponivel(contexto, emails)

    @classmethod
    def reserva_cancelada(cls, contexto, emails):
        EmailService.reserva_cancelada(contexto, emails)
