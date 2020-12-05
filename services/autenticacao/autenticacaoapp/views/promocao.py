from rest_framework import viewsets

from ..models import CodigoPromocao
from ..serializers import CodigoPromocaoCreateSerializer
from ..permissions import (
    AutenticadoPermissao,
    PromoverBolsistaPermissao
)

class PromocaoViewSet(viewsets.ModelViewSet):
    serializer_class = CodigoPromocaoCreateSerializer
    queryset = CodigoPromocao.objects.all()
    permission_classes = [
        AutenticadoPermissao
    ]
    
    def get_permissions(self):
        if self.action == 'create':
            return [
                AutenticadoPermissao(),
                PromoverBolsistaPermissao()
            ]
        return super().get_permissions()
