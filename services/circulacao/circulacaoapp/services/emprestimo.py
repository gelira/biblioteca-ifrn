import os
from django.utils.timezone import localtime

from circulacao.celery import app

from ..models import Emprestimo
from .notificacao import NotificacaoService

CIRCULACAO_QUEUE = os.getenv('PROJECT_NAME')

class EmprestimoService:
    @classmethod
    def emprestimo_avaliado(cls, emprestimo_id):
        Emprestimo.objects.filter(_id=emprestimo_id).update(
            avaliado=True,
            updated=localtime()
        )

    @classmethod
    def get_emprestimo(cls, emprestimo_id):
        e = Emprestimo.objects.filter(_id=emprestimo_id).first()

        if not e:
            return None

        from ..serializers import EmprestimoRetrieveSerializer
        ser = EmprestimoRetrieveSerializer(e)
        return ser.data

    @classmethod
    def enviar_comprovante_emprestimo(cls, contexto, emails):
        NotificacaoService.comprovante_emprestimo(contexto, emails)

    @classmethod
    def call_enviar_comprovante_emprestimo(cls, contexto, emails):
        app.send_task(
            'circulacao.enviar_comprovante_emprestimo',
            args=[contexto, emails],
            queue=CIRCULACAO_QUEUE,
            ignore_result=True
        )
