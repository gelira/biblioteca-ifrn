from rest_framework import serializers

from ..models import Livro

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        exclude = [
            'foto_capa'
        ]

class FotoCapaLivroSerializer(serializers.ModelSerializer):
    def update(self, instance, data):
        instance.foto_capa.delete(save=False)
        return super().update(instance, data)

    class Meta:
        model = Livro
        fields = [
            'foto_capa'
        ]
        extra_kwargs = {
            'foto_capa': {
                'required': True
            }
        }
