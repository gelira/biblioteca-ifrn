import string
import random
from django.db.utils import IntegrityError
from rest_framework import serializers

from ..models import Exemplar, Livro

def gerarCodigo():
    charset = string.ascii_uppercase + string.digits
    chars = [random.choice(charset) for i in range(8)]
    return ''.join(chars)

class ExemplarSerializer(serializers.ModelSerializer):
    livro_id = serializers.UUIDField()

    def validate(self, data):
        try:
            data['livro'] = Livro.objects.filter(_id=data['livro_id']).get()
            return data
        except Livro.DoesNotExist:
            raise serializers.ValidationError('Livro não encontrado')

    def create(self, data):
        while True:
            try:
                exemplar = Exemplar.objects.create(
                    livro=data['livro'],
                    codigo=gerarCodigo()
                )
                return exemplar
            except IntegrityError:
                continue

    class Meta:
        model = Exemplar
        fields = [
            'livro_id',
            'referencia',
            'codigo'
        ]
        extra_kwargs = {
            'codigo': {
                'required': False
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

class ExemplarDisponibilidadeSerializer(serializers.Serializer):
    codigos = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )
    disponivel = serializers.BooleanField()

    def validate_codigos(self, codigos):
        codigos = list(set(codigos))
        quantidade_exemplares = Exemplar.objects.filter(codigo__in=codigos).count()
        if quantidade_exemplares != len(codigos):
            raise serializers.ValidationError('Foram informados códigos inválidos')
        return codigos

    def create(self, data):
        Exemplar.objects.filter(codigo__in=data['codigos']).update(disponivel=data['disponivel'])
        return data
