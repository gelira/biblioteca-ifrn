from django.shortcuts import get_object_or_404
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
            return []
        return [
            AutenticadoPermissao(),
            LivroModificarPermissao()
        ]

    @action(methods=['get'], detail=False, url_path='consulta/(?P<codigo>[^/.]+)')
    def consulta(self, request, codigo):
        exemplar = get_object_or_404(self.get_queryset(), codigo=codigo)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(exemplar)
        
        return Response(data=serializer.data, status=200)
