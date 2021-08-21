from rest_framework.settings import api_settings
from rest_framework_simplejwt.exceptions import TokenError

from ..tokens import AcessoToken
from ..models import Usuario

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
            if user:
                return { 
                    'user_id': user_id 
                }
            
            raise Exception({
                'error': {
                    'detail': 'Token inválido'
                },
                'status': 401
            })

        except TokenError as e:
            raise Exception({
                'error': {
                    'detail': str(e)
                },
                'status': 401
            })
