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

    @classmethod
    def load_info_moderador(cls, contato, contexto):
        contexto['nome_moderador'] = contato.nome
        contexto['matricula_moderador'] = contato.matricula
        return contexto

    @classmethod
    def comprovante_emprestimo(cls, contexto):
        usuario = cls.get_contato(contexto['usuario_id'])
        atendente = cls.get_contato(contexto['atendente_id'])

        contexto = cls.load_info_usuario(usuario, contexto)
        contexto = cls.load_info_atendente(atendente, contexto)

        emails = cls.get_emails_contato(usuario)

        EmailService.comprovante_emprestimo(contexto, emails)

    @classmethod
    def comprovante_devolucao(cls, contexto):
        usuario = cls.get_contato(contexto['usuario_id'])
        atendente = cls.get_contato(contexto['atendente_id'])

        contexto = cls.load_info_usuario(usuario, contexto)
        contexto = cls.load_info_atendente(atendente, contexto)

        emails = cls.get_emails_contato(usuario)

        EmailService.comprovante_devolucao(contexto, emails)

    @classmethod
    def reserva_disponivel(cls, contexto):
        usuario = cls.get_contato(contexto['usuario_id'])
        contexto = cls.load_info_usuario(usuario, contexto)
        emails = cls.get_emails_contato(usuario)

        EmailService.reserva_disponivel(contexto, emails)

    @classmethod
    def reserva_cancelada(cls, contexto):
        usuario = cls.get_contato(contexto['usuario_id'])
        contexto = cls.load_info_usuario(usuario, contexto)
        emails = cls.get_emails_contato(usuario)

        EmailService.reserva_cancelada(contexto, emails)

    @classmethod
    def avaliacao_moderada(cls, contexto):
        usuario = cls.get_contato(contexto['usuario_id'])
        moderador = cls.get_contato(contexto['moderador_id'])

        contexto = cls.load_info_usuario(usuario, contexto)
        contexto = cls.load_info_moderador(moderador, contexto)
        emails = cls.get_emails_contato(usuario)

        EmailService.avaliacao_moderada(contexto, emails)

    @classmethod
    def avaliacao_publicada(cls, contexto):
        usuario = cls.get_contato(contexto['usuario_id'])
        moderador = cls.get_contato(contexto['moderador_id'])

        contexto = cls.load_info_usuario(usuario, contexto)
        contexto = cls.load_info_moderador(moderador, contexto)
        emails = cls.get_emails_contato(usuario)

        EmailService.avaliacao_publicada(contexto, emails)

    @classmethod
    def comprovante_renovacao(cls, contexto):
        usuario = cls.get_contato(contexto['usuario_id'])
        contexto = cls.load_info_usuario(usuario, contexto)

        atendente_id = contexto.get('atendente_id')
        if atendente_id:
            atendente = cls.get_contato(atendente_id)
            contexto = cls.load_info_atendente(atendente, contexto)

        emails = cls.get_emails_contato(usuario)

        EmailService.comprovante_renovacao(contexto, emails)


    @classmethod
    def comprovante_reserva(cls, contexto):
        usuario = cls.get_contato(contexto['usuario_id'])
        contexto = cls.load_info_usuario(usuario, contexto)

        emails = cls.get_emails_contato(usuario)

        EmailService.comprovante_reserva(contexto, emails)

    @classmethod
    def comprovante_reserva_cancelada(cls, contexto):
        usuario = cls.get_contato(contexto['usuario_id'])
        contexto = cls.load_info_usuario(usuario, contexto)

        emails = cls.get_emails_contato(usuario)

        EmailService.comprovante_reserva_cancelada(contexto, emails)
