from django.conf import settings
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from ..serializers import LoginSerializer, UsuarioUpdateSerializer
from ..services import AutenticacaoService

class AutenticacaoViewSet(ViewSet):
    @action(methods=['get', 'put'], detail=False, url_path='informacoes')
    def informacoes(self, request):
        if request.method.lower() == 'put':
            return self.atualizar_informações(request)

        usuario_id = str(request.user.usuario._id)
        
        try:
            data = AutenticacaoService.informacoes_usuario(usuario_id)
            return Response(data=data)
        
        except Exception as e:
            arg = e.args[0]
            
            if isinstance(arg, dict):
                return Response(
                    data=arg.get('error'), 
                    status=arg.get('status', 500)
                )
            
            raise e

    @action(methods=['get'], detail=False, url_path='consulta')
    def consulta(self, request):
        _id = request.GET.get('id')
        matricula = request.GET.get('matricula')
        
        if not _id and not matricula:
            _id = str(request.user.usuario._id)

        try:
            data = AutenticacaoService.consulta_usuario(_id, matricula)
            return Response(data=data)
        
        except Exception as e:
            arg = e.args[0]
            
            if isinstance(arg, dict):
                return Response(
                    data=arg.get('error'), 
                    status=arg.get('status', 500)
                )
            
            raise e

    @action(methods=['post'], detail=False, url_path='token', authentication_classes=[], permission_classes=[])
    def token(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.validated_data

        try:
            login_data = AutenticacaoService.login_suap(data['username'], data['password'])
            return Response(data=login_data)
        
        except Exception as e:
            arg = e.args[0]
            
            if isinstance(arg, dict):
                return Response(
                    data=arg.get('error'), 
                    status=arg.get('status', 500)
                )
            
            raise e

    @action(methods=['post'], detail=False, url_path='token-local', authentication_classes=[], permission_classes=[])
    def token_local(self, request):
        if not settings.DEBUG:
            return Response(status=403)

        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.validated_data

        try:
            login_data = AutenticacaoService.login_local(data['username'], data['password'])
            return Response(data=login_data)
        
        except Exception as e:
            arg = e.args[0]
            
            if isinstance(arg, dict):
                return Response(
                    data=arg.get('error'), 
                    status=arg.get('status', 500)
                )
            
            raise e

    @action(methods=['get'], detail=False, url_path='verificar')
    def verificar(self, request):
        return Response({
            '_id': request.user.usuario._id
        })

    def atualizar_informações(self, request):
        ser = UsuarioUpdateSerializer(
            instance=request.user.usuario,
            data=request.data
        )
        ser.is_valid(raise_exception=True)
        ser.save()
        
        return Response(status=200)
