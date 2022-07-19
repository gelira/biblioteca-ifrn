from rest_framework import viewsets

from ..models import Perfil
from ..serializers import PerfilSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    serializer_class = PerfilSerializer
    queryset = Perfil.objects.all()
    permission_classes = []
