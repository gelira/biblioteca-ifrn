from uuid import UUID
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from .. import serializers
from ..models import Exemplar
from ..permissions import (
    AutenticadoPermissao,
    LivroModificarPermissao,
    CirculacaoServicePermissao
)
from ..services import ExemplarService

class ExemplarViewSet(viewsets.ModelViewSet):
    queryset = Exemplar.objects.all()
    serializer_class = serializers.ExemplarSerializer
    permission_classes = [AutenticadoPermissao, LivroModificarPermissao]

    @action(methods=['get'], detail=False, url_path='consulta/(?P<codigo>[^/.]+)', authentication_classes=[], permission_classes=[])
    def consulta(self, request, codigo):
        ser = self.get_serializer(ExemplarService.consulta_codigo_exemplar(codigo))
        return Response(ser.data)

    @action(methods=['patch'], detail=False, url_path='emprestados')
    def emprestados(self, request):
        codigos = self.codigos(request)
        ExemplarService.exemplares_emprestados(codigos)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['patch'], detail=False, url_path='devolvidos')
    def devolvidos(self, request):
        codigos = self.codigos(request)
        ExemplarService.exemplares_devolvidos(codigos)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        qs = super().get_queryset()

        try:
            livro_id = self.request.GET.get('livro_id')
            qs = qs.filter(livro___id=UUID(livro_id))
        except:
            pass

        return qs

    def codigos(self, request):
        ser = serializers.CodigosExemplaresSerializers(data=request.data)
        ser.is_valid(raise_exception=True)

        return ser.validated_data['codigos']

    def get_permissions(self):
        if self.action in ['emprestados', 'devolvidos']:
            return [
                AutenticadoPermissao(),
                CirculacaoServicePermissao()
            ]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'consulta':
            return serializers.ExemplarConsultaSerializer

        return super().get_serializer_class()
