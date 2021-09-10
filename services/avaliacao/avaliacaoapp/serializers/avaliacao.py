from rest_framework import serializers

from ..models import (
    Avaliacao,
    Tag
)
from ..services import (
    CirculacaoService,
    CatalogoService
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
        if value < 1 or value > 5:
            raise serializers.ValidationError('Nota deve estar entre 1 e 5')
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

        retorno = super().create(data)
        CirculacaoService.emprestimo_avaliado(emprestimo_id)
        CatalogoService.atualizar_nota(livro_id, nota)

        return retorno

    def validar_emprestimo(self, emprestimo_id):
        if Avaliacao.objects.filter(emprestimo_id=emprestimo_id).exists():
            raise serializers.ValidationError('Empréstimo já avaliado')
        
        try:
            emprestimo = CirculacaoService.get_emprestimo(emprestimo_id)
            if not emprestimo:
                raise serializers.ValidationError('Empréstimo não encontrado')

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
