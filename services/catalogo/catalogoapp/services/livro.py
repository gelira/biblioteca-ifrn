from ..models import Livro
from ..serializers import (
    LivroSerializer,
    LivroRetrieveSerializer
)

class LivroService:
    @classmethod
    def busca_livro(cls, livro_id, **kwargs):
        livro = Livro.objects.filter(_id=livro_id).first()

        if not livro:
            raise Exception({
                'error': {
                    'detail': 'Livro não encontrado'
                },
                'status': 404
            })

        serializer_class = LivroSerializer if kwargs.get('min') \
            else LivroRetrieveSerializer
        
        ser = serializer_class(livro)
        return ser.data
