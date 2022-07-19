from rest_framework import serializers

from ..services import UsuarioService
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

class UsuarioUpdateSerializer(serializers.ModelSerializer):
    def validate_email_pessoal(self, value):
        if UsuarioService.email_pessoal_utilizado(value):
            raise serializers.ValidationError('Email já utilizado')
        return value
    
    def save(self):
        usuario = self.instance
        email_pessoal = self.validated_data['email_pessoal']

        UsuarioService.atualizar_email_pessoal(usuario, email_pessoal)

    class Meta:
        model = Usuario
        fields = [
            'email_pessoal'
        ]
        extra_kwargs = {
            'email_pessoal': {
                'required': True
            }
        }

class SuspensaoUsuarioSerializer(serializers.Serializer):
    usuario_id = serializers.UUIDField()
    dias = serializers.IntegerField(min_value=1)

class SuspensoesUsuariosSerializer(serializers.Serializer):
    suspensoes = serializers.ListField(
        child=SuspensaoUsuarioSerializer(),
        allow_empty=False
    )
