from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from ..models import Usuario, Permissao
from .perfil import PerfilSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    matricula = serializers.SerializerMethodField()
    perfil = PerfilSerializer()
    lista_permissoes = serializers.SerializerMethodField()

    def get_matricula(self, obj):
        return obj.user.username

    def get_lista_permissoes(self, obj):
        retorno = []
        qs = Permissao.objects.filter(usuarios__usuario_id=obj.id)
        for perm in qs.all():
            retorno.append(perm.codigo)
        return retorno

    class Meta:
        model = Usuario
        exclude = [
            'id',
            'user'
        ]

class UsuarioConsultaSerializer(serializers.ModelSerializer):
    matricula = serializers.SerializerMethodField()
    perfil = PerfilSerializer()

    def get_matricula(self, obj):
        return obj.user.username

    class Meta:
        model = Usuario
        fields = [
            'matricula',
            'nome',
            'nome_completo',
            'vinculo',
            'url_foto',
            'perfil',
            'suspensao'
        ]
