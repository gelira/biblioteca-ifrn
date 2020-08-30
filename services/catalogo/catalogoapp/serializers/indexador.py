from rest_framework import serializers

from ..models import Indexador, Livro

class IndexadorSerializer(serializers.ModelSerializer):
    livro_id = serializers.UUIDField()

    def validate(self, data):
        try:
            data['livro'] = Livro.objects.filter(_id=data['livro_id']).get()
            return data
        except Livro.DoesNotExist:
            raise serializers.ValidationError('Livro não encontrado')

    def create(self, data):
        indexador = Indexador.objects.create(
            livro=data['livro'],
            indexador=data['indexador'] 
        )
        return indexador

    class Meta:
        model = Indexador
        fields = [
            'indexador',
            'livro_id'
        ]
