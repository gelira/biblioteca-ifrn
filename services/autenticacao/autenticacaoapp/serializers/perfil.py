from rest_framework import serializers

from ..models import Perfil
from ..services import PerfilService

class PerfilSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['padrao'] = PerfilService.assegurar_perfil_padrao_unico(data['padrao'])
        return data

    class Meta:
        model = Perfil
        fields = '__all__'
