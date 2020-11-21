from rest_framework.viewsets import ModelViewSet

from ..models import Tag
from ..permissions import AutenticadoPermissao
from ..serializers import TagCreateSerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagCreateSerializer
    permission_classes = [
        AutenticadoPermissao
    ]
