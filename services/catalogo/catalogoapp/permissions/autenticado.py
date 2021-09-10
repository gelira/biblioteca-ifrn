from rest_framework.permissions import BasePermission

class AutenticadoPermissao(BasePermission):
    message = 'Usuário não autenticado'

    def has_permission(self, request, view):
        u = request.user
        
        if u is None:
            return False

        if u.is_anonymous:
            return False
        
        return True
