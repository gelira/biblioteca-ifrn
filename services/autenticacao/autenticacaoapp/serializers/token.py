from django.contrib.auth import get_user_model

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenVerifySerializer
)
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.settings import api_settings

from ..suap import SUAP, SUAPUnauthorized
from ..models import Usuario
from ..tokens import AcessoToken

User = get_user_model()

class ObterTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return {
            'token': data['access']
        }

class ObterTokenSUAPSerializer(TokenObtainPairSerializer):
    def checar_usuario(self, suap):
        try:
            self.user = User.objects.get(**{ User.USERNAME_FIELD: suap.username })
        except User.DoesNotExist:
            self.criar_usuario(suap)

    def criar_usuario(self, suap):
        dados = suap.dados_usuario()
        matricula = dados['matricula']
        self.user = User.objects.create_user(matricula, password=matricula)
        Usuario.objects.create(
            user=self.user,
            nome=dados['nome_usual'],
            nome_completo=dados['vinculo']['nome'],
            email_institucional=dados['email'],
            vinculo=dados['tipo_vinculo'].lower(),
            url_foto=dados['url_foto_150x200']
        )

    def validate(self, attrs):
        suap = SUAP(attrs['username'], attrs['password'])
        
        try:
            suap.autenticar()
        except SUAPUnauthorized:
            raise AuthenticationFailed
        
        self.checar_usuario(suap)
        token = AcessoToken.for_user(self.user)
        return {
            'token': str(token)
        }

class VerificarTokenSerializer(TokenVerifySerializer):
    def validate(self, attrs):
        token = AccessToken(attrs['token'])
        user_id = token[api_settings.USER_ID_CLAIM]
        user = User.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        return {
            '_id': user.usuario._id
        }        
