from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import Emprestimo
from ..serializers import (
    EmprestimoCreateSerializer,
    DevolucaoEmprestimosSerializer
)
from ..permissions import (
    AutenticadoPermissao,
    FazerEmprestimoPermissao
)

class EmprestimoViewSet(ModelViewSet):
    queryset = Emprestimo.objects.all()
    permission_classes = [
        AutenticadoPermissao,
        FazerEmprestimoPermissao
    ]

    def get_serializer_class(self):
        if self.action == 'devolucoes':
            return DevolucaoEmprestimosSerializer
        return EmprestimoCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)

    @action(methods=['post'], detail=False, url_path='devolucoes')
    def devolucoes(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)
