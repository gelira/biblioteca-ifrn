from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from ..models import Livro
from ..serializers import (
    LivroSerializer, FotoCapaLivroSerializer
)
from ..permissions import CatalogarPermissao

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    permission_classes = [CatalogarPermissao]
    lookup_value_regex = '[a-f0-9]{8}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{12}'
    
    def get_object(self):
        return get_object_or_404(self.queryset, _id=self.kwargs['pk'])

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
