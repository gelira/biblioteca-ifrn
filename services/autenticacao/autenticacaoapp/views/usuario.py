import uuid
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..authentication import RedisAutenticacao
from ..models import Usuario
from ..serializers import (
    UsuarioSerializer,
    UsuarioConsultaSerializer,
    UsuariosSuspensosSerializer
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

class ConsultaUsuarioView(APIView):
    permission_classes = [
        IsAuthenticated,
        AutenticadoPermissao,
        FazerEmprestimoPermissao
    ]

    def get(self, request, *args, **kwargs):
        usuario = request.user.usuario

        if FazerEmprestimoPermissao().has_permission(request, self):    
            _id = request.GET.get('id')
            matricula = request.GET.get('matricula')
            
            try:
                uuid.UUID(_id)     
            except:
                _id = None

            if _id is not None:
                usuario = get_object_or_404(Usuario.objects.all(), _id=_id)

            elif matricula is not None:
                user = get_object_or_404(User.objects.all(), username=matricula)
                usuario = user.usuario

        serializer = UsuarioConsultaSerializer(usuario)
        return Response(data=serializer.data)

class UsuariosSuspensosView(APIView):
    authentication_classes = [RedisAutenticacao]
    permission_classes = [
        AutenticadoPermissao,
        FazerEmprestimoPermissao
    ]

    def post(self, request, *args, **kwargs):
        serializer = UsuariosSuspensosSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)
