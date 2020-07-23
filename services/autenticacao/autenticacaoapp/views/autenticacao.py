from rest_framework_simplejwt.views import TokenViewBase

from ..serializers import (
    ObterTokenSerializer, ObterTokenSUAPSerializer, VerificarTokenSerializer)

class ObterTokenView(TokenViewBase):
    serializer_class = ObterTokenSUAPSerializer

class VerificarTokenView(TokenViewBase):
    serializer_class = VerificarTokenSerializer
