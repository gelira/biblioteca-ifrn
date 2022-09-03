import io
import base64
from PIL import Image
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
