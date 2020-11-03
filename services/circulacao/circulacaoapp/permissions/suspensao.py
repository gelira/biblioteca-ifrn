from rest_framework.permissions import BasePermission

class AbonarSuspensaoPermissao(BasePermission):
    message = 'Você não tem permissão para executar essa ação'

    def has_permission(self, request, view):
        return 'suspensao.abonar' in request.user['lista_permissoes']
