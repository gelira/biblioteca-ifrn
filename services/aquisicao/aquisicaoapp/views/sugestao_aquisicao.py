from django.db import transaction, models
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import SugestaoAquisicao, Curtida
from ..serializers import (
    SugestaoAquisicaoSerializer,
    SugestaoAquisicaoUpdateSerializer,
)
from ..permissions import (
    AutenticadoPermissao,
    ModificarSugestaoAquisicaoPermissao,
)

class SugestaoAquisicaoViewSet(ModelViewSet):
    lookup_value_regex = '[a-f0-9]{8}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{12}'
    lookup_field = '_id'
    queryset = SugestaoAquisicao.objects.all()
    permission_classes = [
        AutenticadoPermissao,
        ModificarSugestaoAquisicaoPermissao,
    ]

    def get_serializer_class(self):
        per = ModificarSugestaoAquisicaoPermissao()
        if per.user_has_permission(self.request) and self.action in ['update', 'partial_update']:
            return SugestaoAquisicaoUpdateSerializer

        return SugestaoAquisicaoSerializer

    @action(methods=['put'], detail=True, url_path='curtida')
    def curtida(self, request, _id=None):
        usuario_id = request.user['_id']
        sugestao = self.get_object()

        if str(sugestao.usuario_id) != usuario_id:
            with transaction.atomic():
                aux = {
                    'sugestao_aquisicao_id': sugestao.pk,
                    'usuario_id': usuario_id
                }

                c = Curtida.objects.filter(**aux).first()
                if c is None:
                    SugestaoAquisicao.objects.filter(pk=sugestao.pk).update(
                        quantidade_curtidas=models.F('quantidade_curtidas') + 1
                    )
                    aux['aviso'] = bool(request.GET.get('aviso'))
                    Curtida.objects.create(**aux)

                else:
                    SugestaoAquisicao.objects.filter(pk=sugestao.pk).update(
                        quantidade_curtidas=models.F('quantidade_curtidas') - 1
                    )
                    c.delete()

        return Response(status=200)

