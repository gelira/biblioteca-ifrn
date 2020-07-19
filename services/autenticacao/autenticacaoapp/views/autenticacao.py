from rest_framework_simplejwt.views import TokenViewBase

from ..serializers import ObterTokenSerializer, VerificarTokenSerializer

class ObterTokenView(TokenViewBase):
    serializer_class = ObterTokenSerializer

class VerificarTokenView(TokenViewBase):
    serializer_class = VerificarTokenSerializer
