from uuid import UUID
from rest_framework import viewsets

from ..models import LocalizacaoFisica
from ..serializers import LocalizacaoFisicaSerializer
from ..permissions import (
    AutenticadoPermissao,
    LivroModificarPermissao
)

class LocalizacaoFisicaViewSet(viewsets.ModelViewSet):
    queryset = LocalizacaoFisica.objects.all()
    serializer_class = LocalizacaoFisicaSerializer
    permission_classes = [AutenticadoPermissao, LivroModificarPermissao]

    def get_queryset(self):
        qs = super().get_queryset()

        try:
            livro_id = self.request.GET.get('livro_id')
            qs = qs.filter(livro___id=UUID(livro_id))
        except:
            pass

        return qs
