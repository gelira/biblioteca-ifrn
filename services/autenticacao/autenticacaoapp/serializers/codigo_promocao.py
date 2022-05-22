from rest_framework import serializers

from .. import exceptions
from ..services import PromocaoService
from ..models import CodigoPromocao

class CodigoPromocaoCreateSerializer(serializers.ModelSerializer):
    def create(self, data):
        return PromocaoService.create_codigo_promocao(
            self.context['request'].user
        )

    class Meta:
        model = CodigoPromocao
        fields = [
            'codigo'
        ]
        extra_kwargs = {
            'codigo': {
                'read_only': True
            }
        }

class UtilizarCodigoPromocaoSerializer(serializers.Serializer):
    codigo = serializers.CharField(
        min_length=1,
        max_length=20
    )

    def validate(self, data):
        try:
            data['codigo'] = PromocaoService.validate_codigo_promocao(data['codigo'])
            return data

        except exceptions.InvalidCodigoPromocao:
            raise serializers.ValidationError('Código inválido')

    def create(self, data):
        usuario = self.context['request'].user.usuario
        codigo_promocao = data['codigo']

        PromocaoService.use_codigo_promocao(usuario, codigo_promocao)

        return {}
