from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import CodigoPromocao
from ..serializers import (
    CodigoPromocaoCreateSerializer,
    UtilizarCodigoPromocaoSerializer
)
from ..permissions import PromoverBolsistaPermissao

class PromocaoViewSet(viewsets.ModelViewSet):
    queryset = CodigoPromocao.objects.all()
    permission_classes = [
        IsAuthenticated
    ]
    
    def get_serializer_class(self):
        if self.action == 'utilizar_codigo':
            return UtilizarCodigoPromocaoSerializer

        return CodigoPromocaoCreateSerializer

    def get_permissions(self):
        permissions = super().get_permissions()

        if self.action == 'create':
            permissions.append(PromoverBolsistaPermissao())

        return permissions

    @action(methods=['post'], detail=False, url_path='utilizar')
    def utilizar_codigo(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
