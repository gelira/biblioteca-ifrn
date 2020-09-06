from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import serializers

from ..models import Livro, Exemplar
from .exemplar import ExemplarListSerializer

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

class LivroRetrieveSerializer(serializers.ModelSerializer):
    foto_capa = serializers.SerializerMethodField()
    exemplares = serializers.SerializerMethodField()
    localizacoes_fisicas = serializers.SerializerMethodField()
    indexadores = serializers.SerializerMethodField()

    def get_foto_capa(self, obj):
        try:
            return obj.foto_capa.url
        except:
            return None

    def get_exemplares(self, obj):
        exemplares = obj.exemplares.filter(ativo=True).all()
        serializer = ExemplarListSerializer(exemplares, many=True)
        return serializer.data

    def get_localizacoes_fisicas(self, obj):
        localizacoes = obj.localizacoes.filter(ativo=True).all()
        retorno = []
        for l in localizacoes:
            retorno.append(l.localizacao)
        return retorno

    def get_indexadores(self, obj):
        indexadores = obj.indexadores.all()
        retorno = []
        for i in indexadores:
            retorno.append(i.indexador)
        return retorno

    class Meta:
        model = Livro
        exclude = [
            'id'
        ]

class LivroPesquisaSerializer(serializers.Serializer):
    titulo = serializers.CharField(
        required=False
    )
    autor = serializers.CharField(
        required=False
    )
    indexador = serializers.CharField(
        required=False
    )

    def validate(self, data):
        titulo = data.get('titulo')
        autor = data.get('autor')
        indexador = data.get('indexador')
        qs = Livro.objects.all()

        if titulo is not None:
            qs = qs.filter(titulo__icontains=titulo).all()
        elif autor is not None:
            qs = qs.filter(
                Q(autor_principal__icontains=autor) | Q(autores_secundarios__icontains=autor) 
            ).all()
        elif indexador is not None:
            qs = qs.filter(indexadores__indexador__icontains=indexador).all()

        serializer = LivroListSerializer(qs, many=True)
        return serializer.data

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

# Este serializer encontrasse no módulo de livros para resolver
# um problema de importação cíclica que estava acontecendo por
# causa do LivroListSerializer
# A forma mais rápida de resolver foi reescrever o serializer
# neste módulo
class ExemplarConsultaSerializer(serializers.ModelSerializer):
    livro = LivroListSerializer(
        read_only=True
    )
    codigo = serializers.CharField(
        max_length=20
    )

    def validate(self, data):
        self.instance = get_object_or_404(Exemplar.objects.all(), codigo=data['codigo'])
        return data

    class Meta:
        model = Exemplar
        exclude = [
            'id'
        ]
        extra_kwargs = {
            'referencia': {
                'read_only': True
            },
            'disponivel':{
                'read_only': True
            },
            'ativo': {
                'read_only': True
            }
        }
