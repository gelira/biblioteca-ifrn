from rest_framework.viewsets import ModelViewSet

from ..models import Feriado
from ..serializers import FeriadoCreateSerializer

class FeriadoViewSet(ModelViewSet):
    queryset = Feriado.objects.all()
    serializer_class = FeriadoCreateSerializer
    permission_classes = []
