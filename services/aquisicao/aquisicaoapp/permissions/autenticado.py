from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission

class AutenticadoPermissao(BasePermission):
    message = 'Usuário não autenticado'

    def has_permission(self, request, view):
        u = request.user
        if u is None:
            return False

        if isinstance(u, AnonymousUser):
            return False

        return True
