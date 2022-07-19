from rest_framework import serializers
from rest_framework.exceptions import APIException

from ..services import (
    AutenticacaoService, 
    ReservaService, 
    EmprestimoService
)
from ..models import Reserva

class ReservaCreateSerializer(serializers.ModelSerializer):
    def validate_livro_id(self, value):
        livro_id = str(value)
        usuario_id = self.context['request'].user['_id']
        suspensao = self.context['request'].user['suspensao']
        max_livros = self.context['request'].user['perfil']['max_livros']

        try:
            AutenticacaoService.check_usuario_suspenso(usuario_id, suspensao)
            EmprestimoService.check_livro_emprestado_usuario(usuario_id, livro_id)
            ReservaService.check_reservas_usuario(usuario_id, livro_id)
            ReservaService.check_disponibilidade_livro(livro_id)
            ReservaService.check_quantidade_reservas_emprestimos(usuario_id, max_livros)

        except APIException as e:
            raise serializers.ValidationError(str(e))

        return value

    def create(self, data):
        usuario_id = self.context['request'].user['_id']
        livro_id = data['livro_id']

        return ReservaService.create_reserva(usuario_id, livro_id)

    class Meta:
        model = Reserva
        fields = [
            'livro_id'
        ]

class CancelarReservaSerializer(serializers.Serializer):
    reserva = serializers.UUIDField()

    def validate_reserva(self, value):
        usuario_id = self.context['request'].user['_id']

        try:
            return ReservaService.check_reserva_to_cancel(usuario_id, value)

        except APIException as e:
            raise serializers.ValidationError(str(e))

    def create(self, data):
        return ReservaService.cancel_reserva(data['reserva'])
