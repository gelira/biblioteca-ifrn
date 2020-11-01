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

    def get_matricula(self, obj):
        return obj.user.username

    class Meta:
        model = Usuario
        fields = [
            'matricula',
            'nome_completo',
            'vinculo',
            'url_foto'
        ]

class UsuarioSuspensoSerializer(serializers.Serializer):
    usuario_id = serializers.UUIDField()
    dias_suspensao = serializers.IntegerField()

class UsuariosSuspensosSerializer(serializers.Serializer):
    usuarios = serializers.ListField(
        child=UsuarioSuspensoSerializer()
    )

    def create(self, data):
        with transaction.atomic():
            for u in data['usuarios']:
                usuario = Usuario.objects.filter(_id=u['usuario_id']).first()
                if usuario is None:
                    continue

                hoje = timezone.now().date()
                if usuario.suspensao is None or usuario.suspensao < hoje:
                    usuario.suspensao = hoje - timezone.timedelta(days=1)

                usuario.suspensao += timezone.timedelta(days=u['dias_suspensao'])
                usuario.save()

        return {}
