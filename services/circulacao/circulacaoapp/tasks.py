from celery import shared_task, Task

from .services import (
    EmprestimoService,
    ReservaService,
    DevolucaoService
)

class BaseTask(Task):
    autoretry_for = [Exception]
    default_retry_delay = 30
    max_retries = None

class IgnoreResultTask(BaseTask):
    ignore_result = True

@shared_task(name='circulacao.emprestimo_avaliado', base=IgnoreResultTask)
def emprestimo_avaliado(emprestimo_id):
    EmprestimoService.emprestimo_avaliado(emprestimo_id)

@shared_task(name='circulacao.verificar_reserva', base=IgnoreResultTask)
def verificar_reserva(reserva_id):
    ReservaService.verificar_reserva(reserva_id)

@shared_task(name='circulacao.enviar_reserva_disponivel', base=IgnoreResultTask)
def enviar_reserva_disponivel(contexto):
    ReservaService.enviar_reserva_disponivel(contexto)

@shared_task(name='circulacao.enviar_reserva_cancelada', base=IgnoreResultTask)
def enviar_reserva_cancelada(contexto):
    ReservaService.enviar_reserva_cancelada(contexto)

@shared_task(name='circulacao.enviar_comprovante_devolucao', base=IgnoreResultTask)
def enviar_comprovante_devolucao(contexto):
    DevolucaoService.enviar_comprovante_devolucao(contexto)

@shared_task(name='circulacao.enviar_comprovante_emprestimo', base=IgnoreResultTask)
def enviar_comprovante_emprestimo(contexto):
    EmprestimoService.enviar_comprovante_emprestimo(contexto)

@shared_task(name='circulacao.enviar_comprovante_renovacao', base=IgnoreResultTask)
def enviar_comprovante_renovacao(contexto):
    EmprestimoService.enviar_comprovante_renovacao(contexto)

@shared_task(name='circulacao.checar_emprestimo', base=IgnoreResultTask)
def checar_emprestimo(contexto):
    EmprestimoService.checar_emprestimo(contexto)

@shared_task(name='circulacao.agendar_alertas_emprestimo', base=IgnoreResultTask)
def agendar_alertas_emprestimo(contexto):
    EmprestimoService.agendar_alertas_emprestimo(contexto)

@shared_task(name='circulacao.proxima_reserva', base=IgnoreResultTask)
def proxima_reserva(livro_id):
    ReservaService.proxima_reserva(livro_id)

@shared_task(name='circulacao.enviar_comprovante_reserva', base=IgnoreResultTask)
def enviar_comprovante_reserva(contexto):
    ReservaService.enviar_comprovante_reserva(contexto)

@shared_task(name='circulacao.enviar_comprovante_reserva_cancelada', base=IgnoreResultTask)
def enviar_comprovante_reserva_cancelada(contexto):
    ReservaService.enviar_comprovante_reserva_cancelada(contexto)
