from rest_framework.viewsets import ModelViewSet

from ..models import Reserva
from ..serializers import ReservaCreateSerializer
from ..permissions import AutenticadoPermissao

class ReservaViewSet(ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaCreateSerializer
    permission_classes = [
        AutenticadoPermissao
    ]
