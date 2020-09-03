from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from ..models import Usuario, Permissao
from .perfil import PerfilSerializer

class UsuarioSerializer(ModelSerializer):
    matricula = SerializerMethodField()
    perfil = PerfilSerializer()
    lista_permissoes = SerializerMethodField()

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
            '_id',
            'user'
        ]
