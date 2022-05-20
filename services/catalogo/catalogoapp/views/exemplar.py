from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import Exemplar
from ..serializers import ExemplarSerializer
from ..permissions import (
    AutenticadoPermissao,
    LivroModificarPermissao
)
from ..services import ExemplarService

class ExemplarViewSet(viewsets.ModelViewSet):
    queryset = Exemplar.objects.all()
    serializer_class = ExemplarSerializer
    permission_classes = [AutenticadoPermissao, LivroModificarPermissao]

    @action(methods=['get'], detail=False, url_path='consulta/(?P<codigo>[^/.]+)', authentication_classes=[], permission_classes=[])
    def consulta(self, request, codigo):
        data = ExemplarService.consulta_codigo_exemplar(codigo)
        return Response(data=data)
