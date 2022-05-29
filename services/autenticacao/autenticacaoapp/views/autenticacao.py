from django.conf import settings
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status

from .. import serializers
from ..services import AutenticacaoService, UsuarioService

class AutenticacaoViewSet(ViewSet):
    @action(methods=['get', 'put'], detail=False, url_path='informacoes')
    def informacoes(self, request):
        if request.method.lower() == 'put':
            return self.atualizar_informações(request)

        usuario_id = str(request.user.usuario._id)
        usuario = AutenticacaoService.informacoes_usuario(usuario_id)

        data = serializers.UsuarioSerializer(usuario).data

        if request.GET.get('save_cache'):
            AutenticacaoService.save_cache(usuario_id, data)

        return Response(data)

    @action(methods=['get'], detail=False, url_path='consulta')
    def consulta(self, request):
        _id = request.GET.get('id')
        matricula = request.GET.get('matricula')
        
        if not _id and not matricula:
            _id = str(request.user.usuario._id)

        usuario = AutenticacaoService.consulta_usuario(_id, matricula)

        ser = serializers.UsuarioConsultaSerializer(usuario)

        return Response(data=ser.data)

    @action(methods=['post'], detail=False, url_path='token', authentication_classes=[], permission_classes=[])
    def token(self, request):
        ser = serializers.LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.validated_data

        login_data = AutenticacaoService.login_suap(data['username'], data['password'])

        return Response(data=login_data)

    @action(methods=['post'], detail=False, url_path='token-local', authentication_classes=[], permission_classes=[])
    def token_local(self, request):
        if not settings.DEBUG:
            return Response(status=status.HTTP_403_FORBIDDEN)

        ser = serializers.LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.validated_data

        login_data = AutenticacaoService.login_local(data['username'], data['password'])
        
        return Response(data=login_data)

    @action(methods=['get'], detail=False, url_path='verificar')
    def verificar(self, request):
        return Response({
            '_id': request.user.usuario._id
        })

    @action(methods=['post'], detail=False, url_path='suspensoes', authentication_classes=[], permission_classes=[])
    def suspensoes(self, request):
        ser = serializers.SuspensoesUsuariosSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        UsuarioService.suspensoes(ser.validated_data)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='abono-suspensoes', authentication_classes=[], permission_classes=[])
    def abono_suspensoes(self, request):
        ser = serializers.SuspensoesUsuariosSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        UsuarioService.abono_suspensoes(ser.validated_data)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def atualizar_informações(self, request):
        ser = serializers.UsuarioUpdateSerializer(
            instance=request.user.usuario,
            data=request.data
        )
        ser.is_valid(raise_exception=True)
        ser.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
