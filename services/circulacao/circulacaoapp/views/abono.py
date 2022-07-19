from rest_framework.viewsets import ModelViewSet

from ..models import Abono
from ..serializers import AbonoCreateSerializer
from ..permissions import (
    AutenticadoPermissao,
    AbonarSuspensaoPermissao
)

class AbonoViewSet(ModelViewSet):
    queryset = Abono.objects.all()
    serializer_class = AbonoCreateSerializer
    permission_classes = [
        AutenticadoPermissao,
        AbonarSuspensaoPermissao
    ]
