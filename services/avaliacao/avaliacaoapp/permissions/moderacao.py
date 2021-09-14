from rest_framework.permissions import BasePermission

class ModerarPermissao(BasePermission):
    message = 'Você não tem permissão para executar essa ação'

    def has_permission(self, request, view):
        return 'avaliacao.moderar' in request.user['lista_permissoes']
