from rest_framework import serializers

from ..services import AbonoService
from ..models import Abono

class AbonoCreateSerializer(serializers.ModelSerializer):
    emprestimos = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False,
        write_only=True
    )

    def validate(self, data):
        suspensoes, usuarios = AbonoService.validate_suspensoes(data['emprestimos'])

        if not usuarios:
            raise serializers.ValidationError('Nenhuma suspensão encontrada')

        data.update({
            'suspensoes': suspensoes,
            'usuarios': usuarios,
        })

        return data

    def create(self, data):
        usuario_id = self.context['request'].user['_id']
        justificativa = data['justificativa']
        suspensoes = data['suspensoes']
        usuarios = data['usuarios']

        return AbonoService.create_abono(usuario_id, justificativa, suspensoes, usuarios)
    
    class Meta:
        model = Abono
        fields = [
            'emprestimos',
            'justificativa'
        ]
