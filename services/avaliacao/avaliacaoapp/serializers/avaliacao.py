from rest_framework import serializers

from ..models import (
    Avaliacao,
    Tag
)
from .. import calls 

class AvaliacaoCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=True,
        write_only=True
    )

    def validate_tags(self, value):
        return Tag.objects.filter(_id__in=value).all()

    def validate_nota(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Nota deve estar entre 1 e 10')
        return value 

    def validate(self, data):
        emprestimo_id = str(data['emprestimo_id'])
        data['livro_id'] = self.validar_emprestimo(emprestimo_id)
        data['usuario_id'] = self.context['request'].user['_id']

        return data

    def create(self, data):
        usuario_id = data['usuario_id']
        emprestimo_id = str(data['emprestimo_id'])

        retorno = super().create(data)
        calls.circulacao.task_emprestimo_avaliado(emprestimo_id)

        return retorno

    def validar_emprestimo(self, emprestimo_id):
        if Avaliacao.objects.filter(emprestimo_id=emprestimo_id).exists():
            raise serializers.ValidationError('Empréstimo já avaliado')
        
        try:
            r = calls.circulacao.api_get_emprestimo(emprestimo_id, self.context['request'].user['_id'])
            if not r.ok:
                raise serializers.ValidationError('Erro ao buscar informações do empréstimo')

            emprestimo = r.json()
            if emprestimo['avaliado']:
                raise serializers.ValidationError('Empréstimo já avaliado')

            return emprestimo['livro_id']

        except serializers.ValidationError as e:
            raise e

        except:
            raise serializers.ValidationError('Erro de comunicação entre os serviços')

    class Meta:
        model = Avaliacao
        exclude = [
            'id'
        ]
        extra_kwargs = {
            'livro_id': {
                'read_only': True
            },
            'usuario_id': {
                'read_only': True
            }
        }
