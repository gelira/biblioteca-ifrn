from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..serializers import (
    UsuarioSerializer,
    UsuarioConsultaSerializer
)
from ..permissions import (
    AutenticadoPermissao,
    FazerEmprestimoPermissao
)

User = get_user_model()

class InformacoesUsuarioView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = UsuarioSerializer(request.user.usuario)
        return Response(data=serializer.data)

class ConsultaMatriculaUsuarioView(APIView):
    permission_classes = [
        IsAuthenticated,
        AutenticadoPermissao,
        FazerEmprestimoPermissao
    ]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(
            User.objects.all(), 
            username=self.kwargs['matricula']
        )
        serializer = UsuarioConsultaSerializer(user.usuario)
        return Response(data=serializer.data)
