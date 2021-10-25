import os
from copy import deepcopy
from celery import group

from aquisicao.celery import app

from ..models import SugestaoAquisicao
from .notificacao import NotificacaoService

AQUISICAO_QUEUE = os.getenv('PROJECT_NAME')

class SugestaoAquisicaoService:
    @classmethod
    def enviar_alertas_sugestao(cls, contexto):
        sugestao = SugestaoAquisicao.objects.filter(_id=contexto['sugestao_id']).first()

        if not sugestao:
            return

        contexto['aviso_curtida'] = False
        contexto['titulo'] = sugestao.titulo
        contexto['usuario_id'] = str(sugestao.usuario_id)

        tasks = [
            app.signature(
                'aquisicao.enviar_alerta_sugestao',
                args=[deepcopy(contexto)],
                queue=AQUISICAO_QUEUE,
                ignore_result=True    
            )
        ]

        contexto['aviso_curtida'] = True

        for curtida in sugestao.curtidas.filter(aviso=True).all():
            contexto['usuario_id'] = str(curtida.usuario_id)
            tasks.append(
                app.signature(
                    'aquisicao.enviar_alerta_sugestao',
                    args=[deepcopy(contexto)],
                    queue=AQUISICAO_QUEUE,
                    ignore_result=True    
                )
            )

        group(tasks)()

    @classmethod
    def enviar_alerta_sugestao(cls, contexto):
        NotificacaoService.alerta_sugestao_listada(contexto)
    
    @classmethod
    def call_enviar_alertas_sugestao(cls, contexto):
        app.send_task(
            'aquisicao.enviar_alertas_sugestao',
            args=[contexto],
            queue=AQUISICAO_QUEUE,
            ignore_result=True
        )
