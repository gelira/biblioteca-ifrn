from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from ..services import AutenticacaoService

class UsuarioViewSet(ViewSet):
    @action(methods=['get'], detail=False, url_path='informacoes')
    def informacoes(self, request):
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
