import os
import json
from celery import group

from django.db import transaction
from django.utils.timezone import (
    datetime, 
    timedelta, 
    make_aware,
    localtime
)
from django_celery_beat.models import PeriodicTask, ClockedSchedule

from circulacao.celery import app

from ..models import Reserva
from ..utils import calcular_data_limite

from .catalogo import CatalogoService
from .notificacao import NotificacaoService

CIRCULACAO_QUEUE = os.getenv('CIRCULACAO_QUEUE')

class ReservaService:
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

            agora = localtime()
            reserva_id = str(proxima_reserva._id)
            data = calcular_data_limite(1)
            
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
            data = data + timedelta(days=1)

            clock = ClockedSchedule.objects.create(
                clocked_time=make_aware(
                    datetime(
                        year=data.year,
                        month=data.month,
                        day=data.day,
                        hour=2,
                        minute=30
                    )
                )
            )

            PeriodicTask.objects.create(
                clocked=clock,
                name=f'Verificar Reserva {reserva_id}',
                task='circulacao.verificar_reserva',
                args=json.dumps([reserva_id]),
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
        app.send_task(
            'circulacao.enviar_reserva_disponivel',
            args=[contexto],
            queue=CIRCULACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def call_enviar_reserva_cancelada(cls, contexto):
        app.send_task(
            'circulacao.enviar_reserva_cancelada',
            args=[contexto],
            queue=CIRCULACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def call_enviar_reservas_disponiveis(cls, reservas):
        group([
            app.signature(
                'circulacao.enviar_reserva_disponivel',
                args=[reserva],
                queue=CIRCULACAO_QUEUE,
                ignore_result=True
            ) for reserva in reservas
        ])()

    @classmethod
    def call_proximas_reservas(cls, livros):
        group([
            app.signature(
                'circulacao.proxima_reserva',
                args=[livro_id],
                queue=CIRCULACAO_QUEUE,
                ignore_result=True
            ) for livro_id in livros
        ])()

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
        app.send_task(
            'circulacao.enviar_comprovante_reserva',
            args=[contexto],
            queue=CIRCULACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def call_enviar_comprovante_reserva_cancelada(cls, contexto):
        app.send_task(
            'circulacao.enviar_comprovante_reserva_cancelada',
            args=[contexto],
            queue=CIRCULACAO_QUEUE,
            ignore_result=True
        )
