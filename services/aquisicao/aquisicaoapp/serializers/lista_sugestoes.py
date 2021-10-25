from django.db import transaction
from django.utils.timezone import localtime
from rest_framework import serializers

from ..models import (
    ListaSugestoes,
    SugestaoAquisicao,
)
from ..services import ListaSugestoesService

class ListaSugestoesSerializer(serializers.ModelSerializer):
    sugestoes = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False,
        min_length=1,
        write_only=True
    )

    def validate_sugestoes(self, value):
        # Removendo possíveis valores repetidos
        value = list(set(map(lambda x: str(x), value)))

        qs = SugestaoAquisicao.objects.filter(_id__in=value)
        if len(value) != qs.count():
            raise serializers.ValidationError('Há sugestões inexistentes')

        qs = qs.exclude(lista_sugestoes_id=None)
        if qs.exists():
            raise serializers.ValidationError('Há sugestões já incluídas em listas')

        return value

    def create(self, data):
        with transaction.atomic():
            l = ListaSugestoes.objects.create(descricao=data['descricao'])
            SugestaoAquisicao.objects.filter(_id__in=data['sugestoes']).update(
                lista_sugestoes_id=l.pk,
                updated=localtime()
            )
            ListaSugestoesService.call_enviar_alertas_lista(str(l._id))
            return l

    class Meta:
        model = ListaSugestoes
        fields = [
            '_id',
            'descricao',
            'sugestoes',
        ]
        extra_kwargs = {
            '_id': {
                'read_only': True
            }
        }
