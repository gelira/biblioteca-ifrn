from rest_framework import viewsets

from ..models import Exemplar
from ..serializers import ExemplarSerializer
from ..permissions import (
    AutenticadoPermissao,
    LivroModificarPermissao
)

class ExemplarViewSet(viewsets.ModelViewSet):
    queryset = Exemplar.objects.all()
    serializer_class = ExemplarSerializer
    permission_classes = [AutenticadoPermissao, LivroModificarPermissao]
