import uuid
from django.utils import timezone
from rest_framework import serializers

from ..models import (
    CodigoPromocao, 
    Usuario
)

class CodigoPromocaoCreateSerializer(serializers.ModelSerializer):
    def create_codigo(self):
        while True:
            codigo = str(uuid.uuid4())[:6].upper()
            if not CodigoPromocao.objects.filter(
                codigo=codigo,
                validade__gte=timezone.now()
            ).exists():
                return codigo

    def get_usuario(self):
        return Usuario.objects.get(user=self.context['request'].user)

    def create(self, data):
        codigo = self.create_codigo()
        usuario = self.get_usuario()
        validade = timezone.now() + timezone.timedelta(minutes=5)

        return CodigoPromocao.objects.create(
            usuario=usuario,
            codigo=codigo,
            validade=validade
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

