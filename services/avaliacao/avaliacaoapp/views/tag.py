from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.views import Response

from ..models import Tag
from ..permissions import (
    AutenticadoPermissao,
    ModerarPermissao
)
from ..serializers import TagCreateSerializer

class TagViewSet(ModelViewSet):
    lookup_value_regex = '[a-f0-9]{8}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{12}'
    queryset = Tag.objects.all()
    serializer_class = TagCreateSerializer
    permission_classes = [
        AutenticadoPermissao
    ]

    @action(methods=['put'], detail=True, url_path='moderacao', permission_classes=[AutenticadoPermissao, ModerarPermissao])
    def moderar(self, request, pk=None):
        tag = self.queryset.filter(_id=pk).first()
        if tag is None:
            return Response(status=404)
        
        tag.censurada = not tag.censurada
        tag.save() 

        return Response(status=200)
