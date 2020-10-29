from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from ..models import Emprestimo
from ..serializers import EmprestimoCreateSerializer
from ..permissions import (
    AutenticadoPermissao,
    FazerEmprestimoPermissao
)

class EmprestimoViewSet(ModelViewSet):
    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoCreateSerializer
    permission_classes = [
        AutenticadoPermissao,
        FazerEmprestimoPermissao
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)
