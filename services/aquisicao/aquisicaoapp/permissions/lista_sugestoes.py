from rest_framework.permissions import BasePermission

class CriarListaSugestoesPermissao(BasePermission):
    message = 'Você não tem permissão para executar essa ação'

    def has_permission(self, request, view):
        return 'lista_sugestoes.criar' in request.user['lista_permissoes']
