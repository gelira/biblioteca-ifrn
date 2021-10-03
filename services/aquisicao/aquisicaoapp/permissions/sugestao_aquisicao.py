from rest_framework.permissions import BasePermission

class ModificarSugestaoAquisicaoPermissao(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action not in ['update', 'partial_update']:
            return True

        in_lista = obj.lista_sugestoes_id is not None

        if str(obj.usuario_id) == request.user['_id']:
            self.message = 'Sugestão já separada em lista'
            return not in_lista

        if 'lista_sugestoes.criar' in request.user['lista_permissoes']:
            self.message = 'Sugestão ainda não pertence a uma lista'
            return in_lista

        self.message = 'Você não pode modificar essa sugestão'
        return False
