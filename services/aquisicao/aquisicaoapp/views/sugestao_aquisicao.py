from rest_framework.viewsets import ModelViewSet

from ..models import SugestaoAquisicao
from ..serializers import SugestaoAquisicaoSerializer
from ..permissions import AutenticadoPermissao

class SugestaoAquisicaoViewSet(ModelViewSet):
    queryset = SugestaoAquisicao.objects.all()
    serializer_class = SugestaoAquisicaoSerializer
    permission_classes = [
        AutenticadoPermissao
    ]
