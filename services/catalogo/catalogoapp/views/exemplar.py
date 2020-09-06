from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import Exemplar
from ..serializers import (
    ExemplarSerializer,
    ExemplarConsultaSerializer
)
from ..permissions import (
    AutenticadoPermissao,
    LivroModificarPermissao
)

class ExemplarViewSet(viewsets.ModelViewSet):
    queryset = Exemplar.objects.all()

    def get_serializer_class(self):
        if self.action == 'consulta':
            return ExemplarConsultaSerializer
        return ExemplarSerializer

    def get_permissions(self):
        if self.action == 'consulta':
            return [AutenticadoPermissao()]
        return [
            AutenticadoPermissao(),
            LivroModificarPermissao()
        ]

    @action(methods=['post'], detail=False, url_path='consulta')
    def consulta(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=200)
