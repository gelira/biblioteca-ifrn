from rest_framework import serializers

from ..models import Livro

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        exclude = [
            'id',
            'foto_capa'
        ]

class LivroListSerializer(serializers.ModelSerializer):
    foto_capa = serializers.SerializerMethodField()

    def get_foto_capa(self, obj):
        try:
            return obj.foto_capa.url
        except:
            return None

    class Meta:
        model = Livro
        exclude = [
            'id'
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
