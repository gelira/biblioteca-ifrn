from datetime import timedelta
from rest_framework import serializers

from ..models import Feriado, Data

class FeriadoCreateSerializer(serializers.ModelSerializer):
    data_inicio = serializers.DateField(
        write_only=True
    )
    data_fim = serializers.DateField(
        write_only=True,
        required=False
    )

    def create(self, data):
        data_inicio = data.pop('data_inicio')
        data_fim = data.pop('data_fim', data_inicio)
        feriado = super().create(data)
        
        while data_inicio <= data_fim:
            Data.objects.create(
                feriado=feriado,
                dia=data_inicio.day,
                mes=data_inicio.month,
                ano=data_inicio.year
            )
            data_inicio = data_inicio + timedelta(days=1)

        return feriado

    class Meta:
        model = Feriado
        fields = [
            'descricao',
            'data_inicio',
            'data_fim'
        ]
