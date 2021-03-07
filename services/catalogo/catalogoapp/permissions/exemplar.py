from rest_framework.permissions import BasePermission

class AlterarDisponibilidadePermissao(BasePermission):
    message = 'Você não tem permissão para executar essa ação'

    def has_permission(self, request, view):
        return 'exemplar.disponibilidade' in request.user['lista_permissoes']
