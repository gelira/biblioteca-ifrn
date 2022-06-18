import io
import base64
from PIL import Image
from django.db.models import Q
from rest_framework import serializers

from ..models import Livro, Exemplar
from ..services import LivroService
from .exemplar import ExemplarListSerializer

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        exclude = [
            'id',
            'soma_notas'
        ]
        extra_kwargs = {
            'media_notas': {
                'read_only': True
            },
            'quantidade_avaliacoes': {
                'read_only': True
            }
        }

class LivroListSerializer(serializers.ModelSerializer):
    foto_capa = serializers.SerializerMethodField()
    exemplares_disponiveis = serializers.SerializerMethodField()

    def get_foto_capa(self, obj):
        return obj.get_foto_url()

    def get_exemplares_disponiveis(self, obj):
        return obj.exemplares.filter(ativo=True, disponivel=True, referencia=False).count()

    class Meta:
        model = Livro
        exclude = [
            'id',
            'soma_notas'
        ]

class LivroRetrieveSerializer(serializers.ModelSerializer):
    foto_capa = serializers.SerializerMethodField()
    exemplares = serializers.SerializerMethodField()
    exemplares_disponiveis = serializers.SerializerMethodField()
    localizacoes_fisicas = serializers.SerializerMethodField()
    indexadores = serializers.SerializerMethodField()

    def get_foto_capa(self, obj):
        return obj.get_foto_url()

    def get_exemplares(self, obj):
        exemplares = obj.exemplares.filter(ativo=True).all()
        serializer = ExemplarListSerializer(exemplares, many=True)
        return serializer.data

    def get_exemplares_disponiveis(self, obj):
        return obj.exemplares.filter(ativo=True, disponivel=True, referencia=False).count()

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
            'id',
            'soma_notas'
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

class FotoCapaLivroSerializer(serializers.Serializer):
    foto_capa = serializers.CharField()

    def validate_foto_capa(self, value):
        try:
            foto_bytes = base64.b64decode(value)
            foto_bytesio = io.BytesIO(foto_bytes)
            Image.open(foto_bytesio)

            return value

        except:
            raise serializers.ValidationError('Arquivo inválido')

    def save(self):
        livro = self.instance

        livro_id = str(livro._id)
        livro_pk = livro.pk
        foto_base64 = self.validated_data['foto_capa']

        LivroService.call_upload_foto_capa(livro_id, livro_pk, foto_base64)

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

class AtualizacaoNotaLivroSerializer(serializers.Serializer):
    livro_id = serializers.UUIDField()
    nota = serializers.IntegerField()

# Este serializer encontra-se no módulo de livros para resolver
# um problema de importação cíclica que estava acontecendo por
# causa do LivroListSerializer
# A forma mais rápida de resolver foi reescrever o serializer
# neste módulo
class ExemplarConsultaSerializer(serializers.ModelSerializer):
    livro = LivroListSerializer(
        read_only=True
    )

    class Meta:
        model = Exemplar
        exclude = [
            'id'
        ]
