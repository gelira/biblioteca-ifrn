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
            'nome_completo',
            'vinculo',
            'url_foto',
            'perfil',
            'suspensao'
        ]

class UsuarioDiasSerializer(serializers.Serializer):
    usuario_id = serializers.UUIDField()
    dias = serializers.IntegerField()

class UsuariosSuspensosSerializer(serializers.Serializer):
    usuarios = serializers.ListField(
        child=UsuarioDiasSerializer()
    )

    def create(self, data):
        hoje = timezone.now().date()
        with transaction.atomic():
            for u in data['usuarios']:
                dias_suspensao = int(u['dias'])
                if dias_suspensao <= 0:
                    continue

                usuario = Usuario.objects.filter(_id=u['usuario_id']).first()
                if usuario is None:
                    continue

                if usuario.suspensao is None or usuario.suspensao < hoje:
                    usuario.suspensao = hoje - timezone.timedelta(days=1)

                usuario.suspensao += timezone.timedelta(days=dias_suspensao)
                usuario.save()

        return {}
