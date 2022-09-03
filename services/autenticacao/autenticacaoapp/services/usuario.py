from django.utils import timezone
from django.db import transaction

from .. import exceptions
from ..models import Usuario
from .notificacao import NotificacaoService

class UsuarioService:
    @classmethod
    def validacao(cls, usuario_id):
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

    @classmethod
    def email_pessoal_utilizado(cls, email):
        return Usuario.objects.filter(email_pessoal=email).exists()

    @classmethod
    def atualizar_email_pessoal(cls, usuario, email_pessoal):
        with transaction.atomic():
            usuario.email_pessoal = email_pessoal
            usuario.save()

            NotificacaoService.call_salvar_contato(
                str(usuario._id),
                {
                    'nome': usuario.nome,
                    'matricula': usuario.user.username,
                    'email_institucional': usuario.email_institucional,
                    'email_pessoal': email_pessoal,
                }
            )
