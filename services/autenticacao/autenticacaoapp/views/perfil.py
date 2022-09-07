from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Perfil
from ..serializers import PerfilSerializer
from ..permissions import GerenciarPerfilPermissao

class PerfilViewSet(viewsets.ModelViewSet):
    serializer_class = PerfilSerializer
    queryset = Perfil.objects.all()
    permission_classes = [
        IsAuthenticated,
        GerenciarPerfilPermissao
    ]
