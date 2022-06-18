from rest_framework.exceptions import APIException

from ..models import Avaliacao
from ..services import CirculacaoService

class AvaliacaoService:
    @classmethod
    def validar_emprestimo(cls, emprestimo_id, usuario_id):
        if Avaliacao.objects.filter(emprestimo_id=emprestimo_id).exists():
            raise APIException('Empréstimo já avaliado')
        
        emprestimo = CirculacaoService.get_emprestimo(emprestimo_id, usuario_id)
        if not emprestimo:
            raise APIException('Empréstimo não encontrado')

        if emprestimo['avaliado']:
            raise APIException('Empréstimo já avaliado')

        return emprestimo

    @classmethod
    def validar_nota(cls, nota):
        if nota < 1 or nota > 5:
            raise APIException('Nota deve estar entre 1 e 5')
