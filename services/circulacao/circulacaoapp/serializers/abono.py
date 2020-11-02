from rest_framework import serializers

from ..models import Abono

class AbonoCreateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        data['usuario_id'] = self.context['request'].user['_id']
        print(data)
        return data

    def create(self, data):
        return Abono.objects.create(
            usuario_id=data['usuario_id'],
            justificativa=data['justificativa']
        )
    
    class Meta:
        model = Abono
        fields = [
            'justificativa'
        ]
