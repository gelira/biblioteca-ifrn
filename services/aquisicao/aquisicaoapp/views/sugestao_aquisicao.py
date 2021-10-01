from django.db import transaction, models
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import SugestaoAquisicao, Curtida
from ..serializers import SugestaoAquisicaoSerializer
from ..permissions import AutenticadoPermissao

class SugestaoAquisicaoViewSet(ModelViewSet):
    lookup_value_regex = '[a-f0-9]{8}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{12}'
    lookup_field = '_id'
    queryset = SugestaoAquisicao.objects.all()
    serializer_class = SugestaoAquisicaoSerializer
    permission_classes = [
        AutenticadoPermissao
    ]

    @action(methods=['put'], detail=True, url_path='curtida')
    def curtida(self, request, _id=None):
        sugestao = self.get_object()

        with transaction.atomic():
            aux = {
                'sugestao_aquisicao_id': sugestao.pk,
                'usuario_id': request.user['_id']
            }

            c = Curtida.objects.filter(**aux).first()
            if c is None:
                SugestaoAquisicao.objects.update(
                    quantidade_curtidas=models.F('quantidade_curtidas') + 1
                )
                aux['aviso'] = bool(request.GET.get('aviso'))
                Curtida.objects.create(**aux)

            else:
                SugestaoAquisicao.objects.update(
                    quantidade_curtidas=models.F('quantidade_curtidas') - 1
                )
                c.delete()

            return Response(status=200)

