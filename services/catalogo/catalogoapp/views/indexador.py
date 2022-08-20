from uuid import UUID
from rest_framework import viewsets

from ..models import Indexador
from ..serializers import IndexadorSerializer
from ..permissions import (
    AutenticadoPermissao,
    LivroCatalogarPermissao
)

class IndexadorViewSet(viewsets.ModelViewSet):
    queryset = Indexador.objects.all()
    serializer_class = IndexadorSerializer
    permission_classes = [AutenticadoPermissao, LivroCatalogarPermissao]

    def get_queryset(self):
        qs = super().get_queryset()

        try:
            livro_id = self.request.GET.get('livro_id')
            qs = qs.filter(livro___id=UUID(livro_id))
        except:
            pass

        return qs
