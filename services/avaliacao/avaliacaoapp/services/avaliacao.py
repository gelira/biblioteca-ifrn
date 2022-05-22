from .. import exceptions
from ..models import Avaliacao
from ..services import CirculacaoService

class AvaliacaoService:
    @classmethod
    def validar_emprestimo(cls, emprestimo_id, usuario_id):
        if Avaliacao.objects.filter(emprestimo_id=emprestimo_id).exists():
            raise exceptions.InvalidEmprestimo('Empréstimo já avaliado')
        
        emprestimo = CirculacaoService.get_emprestimo(emprestimo_id, usuario_id)
        if not emprestimo:
            raise exceptions.InvalidEmprestimo('Empréstimo não encontrado')

        if emprestimo['avaliado']:
            raise exceptions.InvalidEmprestimo('Empréstimo já avaliado')

        return emprestimo
