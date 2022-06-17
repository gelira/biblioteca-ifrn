import os

from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from .. import exceptions
from ..models import Reserva, Emprestimo

from .base import (
    send_task,
    send_task_group, 
    save_clocked_task,
    save_batch_clocked_tasks, 
    datetime_name
)
from .catalogo import CatalogoService
from .notificacao import NotificacaoService
from .feriado import FeriadoService

CIRCULACAO_QUEUE = os.getenv('CIRCULACAO_QUEUE')

class ReservaService:
    task_proxima_reserva = 'circulacao.proxima_reserva'
    task_enviar_comprovante_reserva = 'circulacao.enviar_comprovante_reserva'
    task_enviar_comprovante_reserva_cancelada = 'circulacao.enviar_comprovante_reserva_cancelada'
    task_verificar_reserva = 'circulacao.verificar_reserva'
    task_enviar_reserva_disponivel = 'circulacao.enviar_reserva_disponivel'
    task_enviar_reserva_cancelada = 'circulacao.enviar_reserva_cancelada'

    @classmethod
    def base_queryset(cls, **kwargs):
        hoje = kwargs.pop('hoje', None)
    
        if not hoje:
            hoje = timezone.localdate()

        qs = Reserva.objects.filter(
            Q(disponibilidade_retirada=None) | Q(disponibilidade_retirada__gte=hoje),
            cancelada=False,
            emprestimo_id=None
        )

        if len(kwargs) > 0:
            qs = qs.filter(**kwargs)

        return qs

    @classmethod
    def check_reservas_usuario(cls, usuario_id, livro_id):
        if cls.base_queryset(usuario_id=usuario_id, livro_id=livro_id).exists():
            raise exceptions.ReservaVigente

    @classmethod
    def check_disponibilidade_livro(cls, livro_id):
        livro = CatalogoService.busca_livro(livro_id)

        exemplares_disponiveis = livro['exemplares_disponiveis']

        if exemplares_disponiveis > 0:
            if cls.base_queryset(livro_id=livro_id).count() < exemplares_disponiveis:
                raise exceptions.ExemplaresDisponiveis

    @classmethod
    def check_quantidade_reservas_emprestimos(cls, usuario_id, max_livros):
        emprestimos = Emprestimo.objects.filter(
            usuario_id=usuario_id,
            data_devolucao=None
        ).count()

        reservas = cls.base_queryset(usuario_id=usuario_id).count()

        if (emprestimos + reservas + 1) > max_livros:
            raise exceptions.LimiteEmprestimosReservas

    @classmethod
    def create_reserva(cls, usuario_id, livro_id):
        agora = timezone.localtime()
        agora_data = agora.strftime('%d/%m/%Y')
        agora_hora = agora.strftime('%H:%M:%S')

        with transaction.atomic():
            reserva = Reserva.objects.create(
                usuario_id=usuario_id,
                livro_id=livro_id
            )

            cls.call_enviar_comprovante_reserva({
                'usuario_id': usuario_id,
                'livro_id': livro_id,
                'data': agora_data,
                'hora': agora_hora,
            })

            return reserva

    @classmethod
    def check_reserva_to_cancel(cls, usuario_id, reserva_id):
        reserva = Reserva.objects.filter(
            usuario_id=usuario_id,
            _id=reserva_id
        ).first()

        if reserva is None:
            raise exceptions.ReservaNotFound

        if reserva.cancelada:
            raise exceptions.ReservaCancelada

        if reserva.emprestimo_id is not None:
            raise exceptions.ReservaAtendida

        return reserva

    @classmethod
    def cancel_reserva(cls, reserva):
        usuario_id = str(reserva.usuario_id)
        livro_id = str(reserva.livro_id)

        agora = timezone.localtime()
        agora_data = agora.strftime('%d/%m/%Y')
        agora_hora = agora.strftime('%H:%M:%S')

        livros = []

        with transaction.atomic():
            reserva.cancelada = True
            reserva.save()

            if reserva.disponibilidade_retirada is not None:
                livros.append(livro_id)

            cls.call_enviar_comprovante_reserva_cancelada({
                'usuario_id': usuario_id,
                'livro_id': livro_id,
                'data': agora_data,
                'hora': agora_hora,
            })

            if livros: 
                cls.call_proximas_reservas(livros)

            return {}

    @classmethod
    def proxima_reserva(cls, livro_id):
        with transaction.atomic():
            proxima_reserva = Reserva.objects.filter(
                livro_id=livro_id,
                disponibilidade_retirada=None,
                emprestimo_id=None,
                cancelada=False
            ).first()

            if not proxima_reserva:
                return

            agora = timezone.localtime()
            reserva_id = str(proxima_reserva._id)
            data = FeriadoService.calcular_data_limite(1)
            
            proxima_reserva.disponibilidade_retirada = data
            proxima_reserva.save()

            contexto = {
                'usuario_id': str(proxima_reserva.usuario_id),
                'livro_id': str(proxima_reserva.livro_id),
                'data': agora.strftime('%d/%m/%Y'),
                'hora': agora.strftime('%H:%M:%S'),
                'data_limite': data.strftime('%d/%m/%Y')
            }

            cls.agendar_verificacao(reserva_id, data)
            cls.call_enviar_reserva_disponivel(contexto)

    @classmethod
    def agendar_verificacao(cls, reserva_id, data):
        with transaction.atomic():
            name = datetime_name(cls.task_verificar_reserva)

            dt = timezone.make_aware(
                timezone.datetime(
                    year=data.year,
                    month=data.month,
                    day=data.day,
                    hour=2,
                    minute=30
                )
            )

            save_clocked_task(
                dt=dt, 
                delay_seconds=24*60*60,
                name=name,
                task=cls.task_verificar_reserva,
                headers={ 'periodic_task_name': name },
                args=[reserva_id],
                queue=CIRCULACAO_QUEUE,
                one_off=True
            )

    @classmethod
    def verificar_reserva(cls, reserva_id):
        with transaction.atomic():
            reserva = Reserva.objects.filter(
                _id=reserva_id,
                emprestimo_id=None,
                cancelada=False
            ).first()

            if not reserva:
                return

            livro_id = str(reserva.livro_id)

            reserva.cancelada = True
            reserva.save()

            contexto = {
                'usuario_id': str(reserva.usuario_id),
                'livro_id': livro_id,
                'data_limite': reserva.disponibilidade_retirada.strftime('%d/%m/%Y')
            }

            cls.proxima_reserva(livro_id)
            cls.call_enviar_reserva_cancelada(contexto)

    @classmethod
    def enviar_reserva_disponivel(cls, contexto):
        livro_id = contexto['livro_id']
        livro = CatalogoService.busca_livro(livro_id, sem_exemplares=True)
        
        contexto.update({
            'titulo_livro': livro['titulo']
        })

        NotificacaoService.reserva_disponivel(contexto)

    @classmethod
    def enviar_reserva_cancelada(cls, contexto):
        livro_id = contexto['livro_id']
        livro = CatalogoService.busca_livro(livro_id, sem_exemplares=True)

        contexto.update({
            'titulo_livro': livro['titulo']
        })

        NotificacaoService.reserva_cancelada(contexto)

    @classmethod
    def call_enviar_reserva_disponivel(cls, contexto):
        ctx = { 'args': [contexto], 'queue': CIRCULACAO_QUEUE }

        try:
            send_task(cls.task_enviar_reserva_disponivel, **ctx)

        except:
            name = datetime_name(cls.task_enviar_reserva_disponivel)
            ctx.update({
                'name': name,
                'task': cls.task_enviar_reserva_disponivel,
                'headers': { 'periodic_task_name': name },
                'one_off': True
            })
            
            save_clocked_task(**ctx)

    @classmethod
    def call_enviar_reserva_cancelada(cls, contexto):
        ctx = { 'args': [contexto], 'queue': CIRCULACAO_QUEUE }

        try:
            send_task(cls.task_enviar_reserva_cancelada, **ctx)

        except:
            name = datetime_name(cls.task_enviar_reserva_cancelada)
            ctx.update({
                'name': name,
                'task': cls.task_enviar_reserva_cancelada,
                'headers': { 'periodic_task_name': name },
                'one_off': True
            })
            
            save_clocked_task(**ctx)

    @classmethod
    def call_proximas_reservas(cls, livros):
        func = lambda x: ({ 'args': [x], 'queue': CIRCULACAO_QUEUE })

        contexts = list(map(func, livros))

        try:
            send_task_group(cls.task_proxima_reserva, contexts)

        except:
            for context in contexts:
                name = datetime_name(cls.task_proxima_reserva)
                context.update({
                    'name': name,
                    'task': cls.task_proxima_reserva,
                    'headers': { 'periodic_task_name': name },
                    'one_off': True
                })

            save_batch_clocked_tasks(contexts=contexts)

    @classmethod
    def enviar_comprovante_reserva(cls, contexto):
        livro = CatalogoService.busca_livro(contexto['livro_id'], sem_exemplares=True)
        contexto['titulo_livro'] = livro['titulo']
        NotificacaoService.comprovante_reserva(contexto)

    @classmethod
    def enviar_comprovante_reserva_cancelada(cls, contexto):
        livro = CatalogoService.busca_livro(contexto['livro_id'], sem_exemplares=True)
        contexto['titulo_livro'] = livro['titulo']
        NotificacaoService.comprovante_reserva_cancelada(contexto)

    @classmethod
    def call_enviar_comprovante_reserva(cls, contexto):
        ctx = { 'args': [contexto], 'queue': CIRCULACAO_QUEUE }

        try:
            send_task(cls.task_enviar_comprovante_reserva, **ctx)

        except:
            name = datetime_name(cls.task_enviar_comprovante_reserva)
            ctx.update({
                'name': name,
                'task': cls.task_enviar_comprovante_reserva,
                'headers': { 'periodic_task_name': name },
                'one_off': True
            })
            
            save_clocked_task(**ctx)

    @classmethod
    def call_enviar_comprovante_reserva_cancelada(cls, contexto):
        ctx = { 'args': [contexto], 'queue': CIRCULACAO_QUEUE }

        try:
            send_task(cls.task_enviar_comprovante_reserva_cancelada, **ctx)

        except:
            name = datetime_name(cls.task_enviar_comprovante_reserva_cancelada)
            ctx.update({
                'name': name,
                'task': cls.task_enviar_comprovante_reserva_cancelada,
                'headers': { 'periodic_task_name': name },
                'one_off': True
            })
            
            save_clocked_task(**ctx)
