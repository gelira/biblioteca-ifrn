import os
from celery import group
from copy import deepcopy
from django.utils.timezone import get_current_timezone

from aquisicao.celery import app

from ..models import ListaSugestoes

AQUISICAO_QUEUE = os.getenv('PROJECT_NAME')

class ListaSugestoesService:
    @classmethod
    def enviar_alertas_lista(cls, lista_sugestoes_id):
        lista = ListaSugestoes.objects.filter(_id=lista_sugestoes_id).first()

        if not lista:
            return

        dt = lista.created.astimezone(get_current_timezone())

        tasks = []
        contexto = { 
            'descricao_lista': lista.descricao,
            'data': dt.strftime('%d/%m/%Y'),
            'hora': dt.strftime('%H:%M:%S'),
        }

        for sugestao in lista.sugestoes.all():
            contexto['sugestao_id'] = str(sugestao._id)
            tasks.append(
                app.signature(
                    'aquisicao.enviar_alertas_sugestao',
                    args=[deepcopy(contexto)],
                    queue=AQUISICAO_QUEUE,
                    ignore_result=True    
                ) 
            )

        group(tasks)()

    @classmethod
    def call_enviar_alertas_lista(cls, lista_sugestoes_id):
        # Countdown necessário para evitar
        # condição de corrida com transação do banco de dados
        app.send_task(
            'aquisicao.enviar_alertas_lista',
            args=[lista_sugestoes_id],
            queue=AQUISICAO_QUEUE,
            ignore_result=True,
            countdown=10
        )
