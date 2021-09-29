import os
import json
from celery import group
from django.utils import timezone
from django.db import transaction
from django_celery_beat.models import PeriodicTask, ClockedSchedule

from circulacao.celery import app

from ..models import Emprestimo
from .notificacao import NotificacaoService
from .catalogo import CatalogoService

CIRCULACAO_QUEUE = os.getenv('PROJECT_NAME')

class EmprestimoService:
    @classmethod
    def emprestimo_avaliado(cls, emprestimo_id):
        Emprestimo.objects.filter(_id=emprestimo_id).update(
            avaliado=True,
            updated=timezone.localtime()
        )

    @classmethod
    def get_emprestimo(cls, emprestimo_id, usuario_id=None):
        qs = Emprestimo.objects.filter(_id=emprestimo_id)

        if usuario_id:
            qs = qs.filter(usuario_id=usuario_id)

        e = qs.first()
        if not e:
            return None

        from ..serializers import EmprestimoRetrieveSerializer
        ser = EmprestimoRetrieveSerializer(e)
        return ser.data

    @classmethod
    def enviar_comprovante_emprestimo(cls, contexto):
        NotificacaoService.comprovante_emprestimo(contexto)

    @classmethod
    def enviar_comprovante_renovacao(cls, contexto):
        livro = CatalogoService.busca_livro(contexto['livro_id'], min=True)
        contexto['titulo'] = livro['titulo']
        NotificacaoService.comprovante_renovacao(contexto)

    @classmethod
    def call_enviar_comprovante_emprestimo(cls, contexto):
        app.send_task(
            'circulacao.enviar_comprovante_emprestimo',
            args=[contexto],
            queue=CIRCULACAO_QUEUE,
            ignore_result=True
        )

    @classmethod
    def call_enviar_comprovantes_renovacao(cls, comprovantes):
        group([
            app.signature(
                'circulacao.enviar_comprovante_renovacao',
                args=[comprovante],
                queue=CIRCULACAO_QUEUE,
                ignore_result=True    
            ) for comprovante in comprovantes
        ])()

    @classmethod
    def checar_emprestimo(cls, contexto):
        e = Emprestimo.objects.filter(_id=contexto['emprestimo_id']).first()
        
        if not e:
            return

        if e.data_devolucao is not None:
            return

        if e.data_limite < timezone.localdate():
            NotificacaoService.alerta_emprestimo_atrasado(contexto)
        else:
            NotificacaoService.alerta_emprestimo_vencendo(contexto)

