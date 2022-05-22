from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import CodigoPromocao
from ..serializers import (
    CodigoPromocaoCreateSerializer,
    UtilizarCodigoPromocaoSerializer
)
from ..permissions import (
    AutenticadoPermissao,
    PromoverBolsistaPermissao
)

class PromocaoViewSet(viewsets.ModelViewSet):
    queryset = CodigoPromocao.objects.all()
    permission_classes = [
        AutenticadoPermissao
    ]
    
    def get_serializer_class(self):
        if self.action == 'utilizar_codigo':
            return UtilizarCodigoPromocaoSerializer

        return CodigoPromocaoCreateSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [
                AutenticadoPermissao(),
                PromoverBolsistaPermissao()
            ]

        return super().get_permissions()

    @action(methods=['patch'], detail=False, url_path='utilizar')
    def utilizar_codigo(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=204)
