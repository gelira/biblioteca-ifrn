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
