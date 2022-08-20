from rest_framework import serializers

from ..services import ExemplarService
from ..models import Exemplar, Livro

class ExemplarSerializer(serializers.ModelSerializer):
    livro_id = serializers.UUIDField(write_only=True)

    def validate(self, data):
        try:
            data['livro'] = Livro.objects.filter(_id=data['livro_id']).get()
            return data
        except Livro.DoesNotExist:
            raise serializers.ValidationError('Livro não encontrado')

    def create(self, data):
        return ExemplarService.create_exemplar(data['livro'], data['referencia'])

    class Meta:
        model = Exemplar
        fields = [
            'id',
            'livro_id',
            'referencia',
            'codigo'
        ]
        extra_kwargs = {
            'codigo': {
                'read_only': True
            },
            'referencia': {
                'default': False
            }
        }

class ExemplarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exemplar
        fields = [
            'id',
            'referencia',
            'codigo'
        ]
        extra_kwargs = {
            'codigo': {
                'read_only': True
            }
        }

class ExemplarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exemplar
        fields = [
            'codigo',
            'referencia',
            'disponivel'
        ]

class CodigosExemplaresSerializers(serializers.Serializer):
    codigos = serializers.ListField(
        child=serializers.CharField(max_length=8, min_length=8),
        allow_empty=False
    )
