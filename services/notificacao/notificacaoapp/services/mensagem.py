from .email import EmailService

class MensagemService:
    @classmethod
    def comprovante_emprestimo(cls, contexto, emails):
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
