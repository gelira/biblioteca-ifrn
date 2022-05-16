from django.db import transaction
from rest_framework import serializers

from ..services import AutenticacaoService
from ..models import (
    Abono,
    Suspensao
)

class AbonoCreateSerializer(serializers.ModelSerializer):
    suspensoes = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False,
        write_only=True
    )

    def validate(self, data):
        suspensoes_id = data['suspensoes']
        suspensoes = []
        usuarios = {}

        for s_id in suspensoes_id:
            suspensao = Suspensao.objects.filter(
                _id=s_id,
                abono_id=None
            ).first()
            
            if suspensao is not None:
                usuario_id = str(suspensao.usuario_id)
                if usuario_id not in usuarios:
                    usuarios[usuario_id] = 0
                
                usuarios[usuario_id] += suspensao.total_dias
                suspensoes.append(s_id)

        if not usuarios:
            raise serializers.ValidationError('Nenhuma suspensão encontrada')

        data.update({
            'usuario_id': self.context['request'].user['_id'],
            'usuarios': usuarios,
            'suspensoes': suspensoes
        })
        return data

    def create(self, data):
        usuarios = data['usuarios']

        with transaction.atomic():
            abono = Abono.objects.create(
                usuario_id=data['usuario_id'],
                justificativa=data['justificativa']
            )

            Suspensao.objects.filter(_id__in=data['suspensoes']).update(abono_id=abono.pk)
            AutenticacaoService.abono_suspensoes(list(map(
                lambda x: ({ 'usuario_id': x, 'dias': usuarios[x] }), usuarios)))
        
            return abono
    
    class Meta:
        model = Abono
        fields = [
            'suspensoes',
            'justificativa'
        ]
