from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from ..models import Usuario

class UsuarioSerializer(ModelSerializer):
    matricula = SerializerMethodField()

    def get_matricula(self, obj):
        return obj.user.username

    class Meta:
        model = Usuario
        exclude = [
            'id',
            '_id',
            'user'
        ]
