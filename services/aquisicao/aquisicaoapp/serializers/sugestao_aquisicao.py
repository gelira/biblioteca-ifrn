from rest_framework import serializers

from ..models import SugestaoAquisicao

class SugestaoAquisicaoSerializer(serializers.ModelSerializer):
    def create(self, data):
        data['usuario_id'] = self.context['request'].user['_id']
        return super().create(data)

    class Meta:
        model = SugestaoAquisicao
        fields = [
            '_id',
            'titulo',
            'autor_principal',
            'autores_secundarios',
            'local_publicacao',
            'editora',
            'ano_publicacao',
            'volume',
            'edicao',
            'paginas',
            'comentario',
        ]
        extra_kwargs = {
            '_id': {
                'read_only': True
            }
        }
