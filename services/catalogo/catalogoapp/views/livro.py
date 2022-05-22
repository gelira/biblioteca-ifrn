from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Livro
from ..permissions import (
    AutenticadoPermissao,
    LivroCatalogarPermissao,
    LivroModificarPermissao
)
from ..services import LivroService
from .. import serializers

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
            return serializers.LivroListSerializer
        
        if self.action == 'pesquisa':
            return serializers.LivroPesquisaSerializer
        
        return serializers.LivroSerializer

    def retrieve(self, request, *args, **kwargs):
        data = LivroService.busca_livro(kwargs['pk'], sem_exemplares=request.GET.get('sem_exemplares'))
        return Response(data)

    @action(methods=['put'], detail=True, url_path='foto-capa')
    def foto_capa(self, request, pk=None):
        livro = self.get_object()
        serializer = serializers.FotoCapaLivroSerializer(data=request.data, instance=livro)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='pesquisa')
    def pesquisa(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(data=serializer.validated_data)

    @action(methods=['patch'], detail=False, url_path='atualizar-nota', authentication_classes=[], permission_classes=[])
    def atualizar_nota(self, request):
        ser = serializers.AtualizacaoNotaLivroSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        livro_id = ser.validated_data['livro_id']
        nota = ser.validated_data['nota']

        LivroService.atualizar_nota(livro_id, nota)

        return Response(status=status.HTTP_204_NO_CONTENT)
