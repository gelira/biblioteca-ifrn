from rest_framework.permissions import BasePermission

class CatalogarPermissao(BasePermission):
    message = 'Você não tem permissão para realizar esta ação'

    def has_permission(self, request, view):
        return 'livro.catalogar' in request.user['lista_permissoes']
