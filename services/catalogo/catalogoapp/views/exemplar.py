from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .. import serializers
from ..models import Exemplar
from ..permissions import (
    AutenticadoPermissao,
    LivroModificarPermissao
)
from ..services import ExemplarService

class ExemplarViewSet(viewsets.ModelViewSet):
    queryset = Exemplar.objects.all()
    serializer_class = serializers.ExemplarSerializer
    permission_classes = [AutenticadoPermissao, LivroModificarPermissao]

    @action(methods=['get'], detail=False, url_path='consulta/(?P<codigo>[^/.]+)', authentication_classes=[], permission_classes=[])
    def consulta(self, request, codigo):
        data = ExemplarService.consulta_codigo_exemplar(codigo)
        return Response(data)

    @action(methods=['patch'], detail=False, url_path='emprestados', authentication_classes=[], permission_classes=[])
    def emprestados(self, request):
        codigos = self.codigos(request)
        ExemplarService.exemplares_emprestados(codigos)

        return Response(status=204)

    @action(methods=['patch'], detail=False, url_path='devolvidos', authentication_classes=[], permission_classes=[])
    def devolvidos(self, request):
        codigos = self.codigos(request)
        ExemplarService.exemplares_devolvidos(codigos)

        return Response(status=204)

    def codigos(self, request):
        ser = serializers.CodigosExemplaresSerializers(data=request.data)
        ser.is_valid(raise_exception=True)

        return ser.validated_data['codigos']
