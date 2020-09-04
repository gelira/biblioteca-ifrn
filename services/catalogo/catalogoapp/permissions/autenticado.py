from rest_framework.permissions import BasePermission

class AutenticadoPermissao(BasePermission):
    message = 'Usuário não autenticado'

    def has_permission(self, request, view):
        return request.user is not None
