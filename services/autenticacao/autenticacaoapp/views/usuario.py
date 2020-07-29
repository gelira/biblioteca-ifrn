from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers import UsuarioSerializer

class InformacoesUsuarioView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = UsuarioSerializer(request.user.usuario)
        return Response(data=serializer.data)
