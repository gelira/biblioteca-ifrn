from rest_framework import viewsets

from ..models import Tag
from ..permissions import AutenticadoPermissao
from ..serializers import TagCreateSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagCreateSerializer
    permission_classes = [
        AutenticadoPermissao
    ]
