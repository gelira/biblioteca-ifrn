import os
from django.db import transaction
from rest_framework import serializers

from ..models import (
    Abono,
    Suspensao
)
from ..tasks import usuarios_abono

PROJECT_NAME = os.getenv('PROJECT_NAME')

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
            suspensao = Suspensao.objects.filter(**{
                '_id': s_id,
                'abono_id': None
            }).first()
            
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
        abono = None
        with transaction.atomic():
            abono = Abono.objects.create(
                usuario_id=data['usuario_id'],
                justificativa=data['justificativa']
            )
            Suspensao.objects.filter(_id__in=data['suspensoes']).update(abono_id=abono.pk)

        usuarios_abono.apply_async([data['usuarios']], queue=PROJECT_NAME)
        return abono
    
    class Meta:
        model = Abono
        fields = [
            'suspensoes',
            'justificativa'
        ]
