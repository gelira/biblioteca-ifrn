from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.views import Response

from ..models import Avaliacao
from ..permissions import (
    AutenticadoPermissao,
    ModerarPermissao
)
from ..serializers import AvaliacaoCreateSerializer

class AvaliacaoViewSet(ModelViewSet):
    lookup_value_regex = '[a-f0-9]{8}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{12}'
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoCreateSerializer
    permission_classes = [
        AutenticadoPermissao
    ]

    @action(methods=['put'], detail=True, url_path='moderacao', permission_classes=[AutenticadoPermissao, ModerarPermissao])
    def moderar(self, request, pk=None):
        avaliacao = self.queryset.filter(_id=pk).first()
        if avaliacao is None:
            return Response(status=404)
        
        avaliacao.censurada = not avaliacao.censurada
        avaliacao.save() 

        return Response(status=200)
