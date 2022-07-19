from rest_framework.permissions import BasePermission

class FazerEmprestimoPermissao(BasePermission):
    message = 'Você não tem permissão para executar essa ação'

    def has_permission(self, request, view):
        return 'emprestimo.fazer' in request.user['lista_permissoes']
