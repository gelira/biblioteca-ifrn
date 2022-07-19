from rest_framework.permissions import BasePermission

class LivroCatalogarPermissao(BasePermission):
    message = 'Você não tem permissão para catalogar livros'

    def has_permission(self, request, view):
        return 'livro.catalogar' in request.user['lista_permissoes']

class LivroModificarPermissao(BasePermission):
    message = 'Você não tem permissão para modificar livros'

    def has_permission(self, request, view):
        return 'livro.modificar' in request.user['lista_permissoes']
