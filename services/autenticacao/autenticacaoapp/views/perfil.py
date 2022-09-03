from rest_framework import viewsets

from ..models import Perfil
from ..serializers import PerfilSerializer
from ..permissions import (
    AutenticadoPermissao,
    GerenciarPerfilPermissao
)

class PerfilViewSet(viewsets.ModelViewSet):
    serializer_class = PerfilSerializer
    queryset = Perfil.objects.all()
    permission_classes = [
        AutenticadoPermissao,
        GerenciarPerfilPermissao
    ]
