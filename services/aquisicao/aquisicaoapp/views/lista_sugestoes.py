from rest_framework.viewsets import ModelViewSet

from ..models import ListaSugestoes
from ..serializers import ListaSugestoesSerializer
from ..permissions import (
    AutenticadoPermissao,
    CriarListaSugestoesPermissao
)

class ListaSugestoesViewSet(ModelViewSet):
    queryset = ListaSugestoes.objects.all()
    serializer_class = ListaSugestoesSerializer
    permission_classes = [
        AutenticadoPermissao,
        CriarListaSugestoesPermissao,
    ]
