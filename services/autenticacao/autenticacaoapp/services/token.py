from rest_framework.settings import api_settings
from rest_framework_simplejwt.exceptions import TokenError

from ..tokens import AcessoToken
from ..models import Usuario
from .. import exceptions

class TokenService:
    @staticmethod
    def gerar_token(user):
        token = AcessoToken.for_user(user)
        return str(token)

    @staticmethod
    def verificar_token(token):
        try:
            claim = api_settings.USER_ID_CLAIM
        except:
            claim = 'user_id'

        try:
            field = api_settings.USER_ID_FIELD
        except:
            field = '_id'

        try:
            validated_token = AcessoToken(token)
            user_id = validated_token[claim]
            
            user = Usuario.objects.filter(**{ field: user_id }).first()
            if not user:
                raise exceptions.InvalidToken
            
            return { 
                'user_id': user_id 
            }

        except TokenError as e:
            raise exceptions.InvalidToken(str(e))
