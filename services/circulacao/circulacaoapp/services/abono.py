from django.db import transaction

from ..models import Abono, Suspensao
from .autenticacao import AutenticacaoService

class AbonoService:
    @classmethod
    def validate_suspensoes(cls, emprestimos_id):
        suspensoes = []
        usuarios = {}

        for e_id in emprestimos_id:
            suspensao = Suspensao.objects.filter(
                emprestimo___id=e_id, 
                abono_id=None
            ).first()
            
            if suspensao is not None:
                usuario_id = str(suspensao.usuario_id)
                if usuario_id not in usuarios:
                    usuarios[usuario_id] = 0
                
                usuarios[usuario_id] += suspensao.total_dias
                suspensoes.append(suspensao._id)

        return suspensoes, usuarios

    @classmethod
    def create_abono(cls, usuario_id, justificativa, suspensoes, usuarios):
        with transaction.atomic():
            abono = Abono.objects.create(
                justificativa=justificativa,
                usuario_id=usuario_id
            )

            Suspensao.objects.filter(_id__in=suspensoes).update(abono_id=abono.pk)
            
            func = lambda x: ({ 'usuario_id': x, 'dias': usuarios[x] })
            AutenticacaoService.abono_suspensoes(list(map(func, usuarios)))
        
            return abono
