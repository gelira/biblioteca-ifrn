from rest_framework import serializers

from ..models import Reserva

class ReservaCreateSerializer(serializers.ModelSerializer):
    def create(self, data):
        return Reserva.objects.create(
            livro_id=data['livro_id'],
            usuario_id=self.context['request'].user['_id']
        )
    
    class Meta:
        model = Reserva
        fields = [
            'livro_id'
        ]
