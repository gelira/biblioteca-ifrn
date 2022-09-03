from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Livro
from ..permissions import (
    AutenticadoPermissao,
    LivroCatalogarPermissao,
    LivroModificarPermissao,
    AvaliacaoServicePermissao
)
from ..services import LivroService
from .. import serializers

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    lookup_value_regex = '[a-f0-9]{8}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{12}'
    
    def get_object(self):
        return get_object_or_404(self.queryset, _id=self.kwargs['pk'])

    def get_permissions(self):
        if self.action == 'atualizar_nota':
            return [
                AutenticadoPermissao(),
                AvaliacaoServicePermissao()
            ]

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
        if self.action == 'retrieve':
            if self.request.GET.get('sem_exemplares'):
                return serializers.LivroSerializer

            return serializers.LivroRetrieveSerializer

        if self.action == 'list':
            return serializers.LivroListSerializer
        
        return serializers.LivroSerializer

    def retrieve(self, request, *args, **kwargs):
        ser = self.get_serializer(LivroService.busca_livro(kwargs['pk']))
        return Response(ser.data)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.action == 'list':
            titulo = self.request.GET.get('titulo')
            autor = self.request.GET.get('autor')
            indexador = self.request.GET.get('indexador')

            if titulo is not None:
                qs = qs.filter(titulo__icontains=titulo)
            
            elif autor is not None:
                qs = qs.filter(
                    Q(autor_principal__icontains=autor) | Q(autores_secundarios__icontains=autor) 
                )

            elif indexador is not None:
                qs = qs.filter(indexadores__indexador__icontains=indexador)

        return qs

    @action(methods=['put'], detail=True, url_path='foto-capa')
    def foto_capa(self, request, pk=None):
        livro = self.get_object()
        serializer = serializers.FotoCapaLivroSerializer(data=request.data, instance=livro)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['patch'], detail=False, url_path='atualizar-nota')
    def atualizar_nota(self, request):
        ser = serializers.AtualizacaoNotaLivroSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        livro_id = ser.validated_data['livro_id']
        nota = ser.validated_data['nota']

        LivroService.atualizar_nota(livro_id, nota)

        return Response(status=status.HTTP_204_NO_CONTENT)
