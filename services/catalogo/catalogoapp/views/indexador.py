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
