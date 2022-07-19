from rest_framework.permissions import BasePermission

class AvaliacaoServicePermissao(BasePermission):
    message = 'Você não tem permissão para executar essa ação'

    def has_permission(self, request, view):
        return 'avaliacao_service' in request.user['lista_permissoes']

class CirculacaoServicePermissao(BasePermission):
    message = 'Você não tem permissão para executar essa ação'

    def has_permission(self, request, view):
        return 'circulacao_service' in request.user['lista_permissoes']
