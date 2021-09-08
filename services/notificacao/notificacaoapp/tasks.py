from celery import shared_task, Task

from .services import MensagemService, ContatoService

class BaseTask(Task):
    autoretry_for = [Exception]
    default_retry_delay = 30
    max_retries = None

class IgnoreResultTask(BaseTask):
    ignore_result = True

@shared_task(name='notificacao.comprovante_emprestimo', base=IgnoreResultTask)
def comprovante_emprestimo(contexto, emails):
    MensagemService.comprovante_emprestimo(contexto, emails)

@shared_task(name='notificacao.comprovante_devolucao', base=IgnoreResultTask)
def comprovante_devolucao(contexto, emails):
    MensagemService.comprovante_devolucao(contexto, emails)

@shared_task(name='notificacao.reserva_disponivel', base=IgnoreResultTask)
def reserva_disponivel(contexto, emails):
    MensagemService.reserva_disponivel(contexto, emails)

@shared_task(name='notificacao.reserva_cancelada', base=IgnoreResultTask)
def reserva_cancelada(contexto, emails):
    MensagemService.reserva_cancelada(contexto, emails)

@shared_task(name='notificacao.salvar_contato', base=IgnoreResultTask)
def salvar_contato(usuario_id, data):
    ContatoService.salvar_contato(usuario_id, data)
