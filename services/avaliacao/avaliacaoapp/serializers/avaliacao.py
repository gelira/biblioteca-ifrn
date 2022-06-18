from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import APIException

from ..models import (
    Avaliacao,
    Tag
)
from ..services import (
    CirculacaoService,
    CatalogoService,
    AvaliacaoService
)

class AvaliacaoCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=True,
        write_only=True
    )

    def validate_tags(self, value):
        return Tag.objects.filter(_id__in=value).all()

    def validate_nota(self, value):
        try:
            AvaliacaoService.validar_nota(value)

        except APIException as e:
            raise serializers.ValidationError(str(e))
        
        return value 

    def validate(self, data):
        emprestimo_id = str(data['emprestimo_id'])
        data['livro_id'] = self.validar_emprestimo(emprestimo_id)
        data['usuario_id'] = self.context['request'].user['_id']

        return data

    def create(self, data):
        emprestimo_id = str(data['emprestimo_id'])
        livro_id = str(data['livro_id'])
        nota = data['nota']

        with transaction.atomic():
            retorno = super().create(data)
            CirculacaoService.call_emprestimo_avaliado(emprestimo_id)
            CatalogoService.call_atualizar_nota(livro_id, nota)

            return retorno

    def validar_emprestimo(self, emprestimo_id):
        usuario_id = self.context['request'].user['_id']
        
        try:
            emprestimo = AvaliacaoService.validar_emprestimo(emprestimo_id, usuario_id)
            return emprestimo['livro_id']

        except APIException as e:
            raise serializers.ValidationError(str(e))

    class Meta:
        model = Avaliacao
        exclude = [
            'id',
            'censurada'
        ]
        extra_kwargs = {
            'livro_id': {
                'read_only': True
            },
            'usuario_id': {
                'read_only': True
            }
        }
