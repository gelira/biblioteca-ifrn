from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Reserva
from ..serializers import (
    ReservaCreateSerializer,
    CancelarReservaSerializer
)
from ..permissions import AutenticadoPermissao

class ReservaViewSet(ModelViewSet):
    queryset = Reserva.objects.all()
    permission_classes = [
        AutenticadoPermissao
    ]

    def get_serializer_class(self):
        if self.action == 'cancelar':
            return CancelarReservaSerializer
        return ReservaCreateSerializer

    @action(methods=['put'], detail=False, url_path='cancelar')
    def cancelar(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)
