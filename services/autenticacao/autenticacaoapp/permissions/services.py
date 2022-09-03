from django.contrib.auth.models import AnonymousUser

from .base import BasePermission

class CirculacaoServicePermissao(BasePermission):
    message = 'Você não tem permissão para realizar essa ação'

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False

        return request.user.usuario.permissoes\
            .filter(permissao__codigo='circulacao_service').exists()
