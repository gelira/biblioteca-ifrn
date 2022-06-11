from django.db import transaction
from rest_framework import serializers

from ..services import FeriadoService
from ..models import Feriado

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

        with transaction.atomic():
            feriado = super().create(data)

            FeriadoService.create_dias_feriado(feriado, data_inicio, data_fim)

            return feriado

    class Meta:
        model = Feriado
        fields = [
            'descricao',
            'data_inicio',
            'data_fim'
        ]
