from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import Exemplar
from ..serializers import (
    ExemplarSerializer,
    ExemplarConsultaSerializer,
    ExemplarDisponibilidadeSerializer
)
from ..permissions import (
    AutenticadoPermissao,
    LivroModificarPermissao,
    FazerEmprestimoPermissao,
    AlterarDisponibilidadePermissao
)

class ExemplarViewSet(viewsets.ModelViewSet):
    queryset = Exemplar.objects.all()

    def get_serializer_class(self):
        if self.action == 'consulta':
            return ExemplarConsultaSerializer

        if self.action in ['exemplares_emprestados', 'exemplares_devolvidos']:
            return ExemplarDisponibilidadeSerializer
        
        return ExemplarSerializer

    def get_permissions(self):
        if self.action == 'consulta':
            return []

        if self.action in ['exemplares_emprestados', 'exemplares_devolvidos']:
            return [
                AutenticadoPermissao(),
                AlterarDisponibilidadePermissao()
            ]

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

    @action(methods=['put'], detail=False, url_path='emprestados')
    def exemplares_emprestados(self, request):
        request.data['disponivel'] = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)

    @action(methods=['put'], detail=False, url_path='devolvidos')
    def exemplares_devolvidos(self, request):
        request.data['disponivel'] = True
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)
