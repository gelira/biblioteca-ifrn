from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from ..models import Livro
from ..serializers import (
    LivroSerializer, 
    LivroListSerializer,
    LivroRetrieveSerializer,
    LivroPesquisaSerializer,
    FotoCapaLivroSerializer
)
from ..permissions import (
    AutenticadoPermissao,
    LivroCatalogarPermissao,
    LivroModificarPermissao
)

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    lookup_value_regex = '[a-f0-9]{8}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{12}'
    
    def get_object(self):
        return get_object_or_404(self.queryset, _id=self.kwargs['pk'])

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [
                AutenticadoPermissao(), 
                LivroModificarPermissao()
            ]
        if self.action in ['create', 'destroy', 'foto_capa']:
            return [
                AutenticadoPermissao(), 
                LivroCatalogarPermissao()
            ]
        return []

    def get_serializer_class(self):
        if self.action == 'list':
            return LivroListSerializer
        if self.action == 'retrieve':
            return LivroRetrieveSerializer
        if self.action == 'pesquisa':
            return LivroPesquisaSerializer
        return LivroSerializer

    @action(methods=['put', 'delete'], detail=True, url_path='foto-capa', parser_classes=[MultiPartParser])
    def foto_capa(self, request, pk=None):
        livro = self.get_object()
        if request.method.lower() == 'delete':
            livro.foto_capa.delete()
            return Response(status=204)

        serializer = FotoCapaLivroSerializer(data=request.data, instance=livro)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=200)

    @action(methods=['post'], detail=False, url_path='pesquisa')
    def pesquisa(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.validated_data, status=200)
