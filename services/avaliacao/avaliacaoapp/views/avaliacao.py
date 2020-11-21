from rest_framework.viewsets import ModelViewSet

from ..models import Avaliacao
from ..permissions import AutenticadoPermissao
from ..serializers import AvaliacaoCreateSerializer

class AvaliacaoViewSet(ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoCreateSerializer
    permission_classes = [
        AutenticadoPermissao
    ]
