import uuid
from django.utils import timezone
from django.db import transaction

from .. import exceptions
from ..models import Usuario

class UsuarioService:
    @classmethod
    def validacao(cls, usuario_id):
        try:
            uuid.UUID(usuario_id)
        except:
            raise exceptions.InvalidUUID

        hoje = timezone.localdate()

        usuario = Usuario.objects.filter(_id=usuario_id).first()
        if usuario is None:
            raise exceptions.UserNotFound

        return hoje, usuario

    @classmethod
    def suspensoes(cls, suspensoes):
        with transaction.atomic():
            for suspensao in suspensoes:
                usuario_id = suspensao['usuario_id']
                dias = suspensao['dias']

                hoje, usuario = cls.validacao(usuario_id)

                if usuario.suspensao is None or usuario.suspensao < hoje:
                    usuario.suspensao = hoje - timezone.timedelta(days=1)

                usuario.suspensao += timezone.timedelta(days=dias)
                usuario.save()

    @classmethod
    def abono_suspensoes(cls, suspensoes):
        with transaction.atomic():
            for suspensao in suspensoes:
                usuario_id = suspensao['usuario_id']
                dias = suspensao['dias']

                hoje, usuario = cls.validacao(usuario_id)

                if usuario.suspensao is None:
                    continue
                
                if usuario.suspensao >= hoje:
                    usuario.suspensao -= timezone.timedelta(days=dias)
                    usuario.save()
