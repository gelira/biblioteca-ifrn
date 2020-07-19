from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenVerifySerializer)
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.settings import api_settings

User = get_user_model()

class ObterTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return {
            'token': data['access']
        }

class VerificarTokenSerializer(TokenVerifySerializer):
    def validate(self, attrs):
        token = AccessToken(attrs['token'])
        user_id = token[api_settings.USER_ID_CLAIM]
        user = User.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        return {
            '_id': user.usuario._id
        }        
