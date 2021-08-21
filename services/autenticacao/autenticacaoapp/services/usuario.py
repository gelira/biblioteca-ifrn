from uuid import UUID
from django.utils import timezone

from ..models import Usuario

class UsuarioService:
    @classmethod
    def validacao(cls, usuario_id, dias):
        UUID(usuario_id)
        hoje = timezone.localdate()

        if dias <= 0:
            raise Exception

        usuario = Usuario.objects.filter(_id=usuario_id).first()
        if usuario is None:
            raise Exception

        return hoje, usuario

    @classmethod
    def suspensao(cls, usuario_id, dias):
        try:
            hoje, usuario = cls.validacao(usuario_id, dias)

            if usuario.suspensao is None or usuario.suspensao < hoje:
                usuario.suspensao = hoje - timezone.timedelta(days=1)

            usuario.suspensao += timezone.timedelta(days=dias)
            usuario.save()

        except:
            return

    @classmethod
    def abono_suspensao(cls, usuario_id, dias):
        try:
            hoje, usuario = cls.validacao(usuario_id, dias)

            if usuario.suspensao is None:
                return
            
            if usuario.suspensao >= hoje:
                usuario.suspensao -= timezone.timedelta(days=dias)
                usuario.save()

        except:
            return
