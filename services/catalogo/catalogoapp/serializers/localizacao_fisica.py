from rest_framework import serializers

from ..models import LocalizacaoFisica, Livro

class LocalizacaoFisicaSerializer(serializers.ModelSerializer):
    livro_id = serializers.UUIDField()

    def validate(self, data):
        try:
            data['livro'] = Livro.objects.filter(_id=data['livro_id']).get()
            return data
        except Livro.DoesNotExist:
            raise serializers.ValidationError('Livro não encontrado')

    def create(self, data):
        return LocalizacaoFisica.objects.create(
            livro=data['livro'],
            localizacao=data['localizacao']
        )

    class Meta:
        model = LocalizacaoFisica
        fields = [
            'livro_id',
            'localizacao'
        ]
