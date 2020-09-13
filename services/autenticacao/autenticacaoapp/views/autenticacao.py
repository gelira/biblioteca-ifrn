from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from ..serializers import (
    ObterTokenSUAPSerializer, 
    ObterTokenLocalSerializer
)

class ObterTokenView(TokenViewBase):
    serializer_class = ObterTokenSUAPSerializer

class ObterTokenLocalView(TokenViewBase):
    serializer_class = ObterTokenLocalSerializer

class VerificarTokenView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            '_id': request.user.usuario._id
        })
