from celery import shared_task, Task

from .services import MensagemService, ContatoService

class BaseTask(Task):
    autoretry_for = [Exception]
    default_retry_delay = 30
    max_retries = None

class IgnoreResultTask(BaseTask):
    ignore_result = True

@shared_task(name='notificacao.comprovante_emprestimo', base=IgnoreResultTask)
def comprovante_emprestimo(contexto):
    MensagemService.comprovante_emprestimo(contexto)

@shared_task(name='notificacao.comprovante_devolucao', base=IgnoreResultTask)
def comprovante_devolucao(contexto):
    MensagemService.comprovante_devolucao(contexto)

@shared_task(name='notificacao.reserva_disponivel', base=IgnoreResultTask)
def reserva_disponivel(contexto):
    MensagemService.reserva_disponivel(contexto)

@shared_task(name='notificacao.reserva_cancelada', base=IgnoreResultTask)
def reserva_cancelada(contexto):
    MensagemService.reserva_cancelada(contexto)

@shared_task(name='notificacao.avaliacao_moderada', base=IgnoreResultTask)
def avaliacao_moderada(contexto):
    MensagemService.avaliacao_moderada(contexto)

@shared_task(name='notificacao.avaliacao_publicada', base=IgnoreResultTask)
def avaliacao_publicada(contexto):
    MensagemService.avaliacao_publicada(contexto)

@shared_task(name='notificacao.salvar_contato', base=IgnoreResultTask)
def salvar_contato(usuario_id, data):
    ContatoService.salvar_contato(usuario_id, data)
