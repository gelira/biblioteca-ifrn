import os
import requests
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from ..models import (
    Reserva,
    Emprestimo
)

CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')

class ReservaCreateSerializer(serializers.ModelSerializer):
    def validate_livro_id(self, value):
        livro_id = str(value)
        self.validar_usuario_suspenso()
        self.validar_emprestimos(livro_id)
        self.validar_reservas(livro_id)
        self.validar_livro(livro_id)
        return value

    def validar_usuario_suspenso(self):
        usuario_id = self.context['request'].user['_id']
        suspensao = self.context['request'].user['suspensao']
        hoje = timezone.now().date()

        if suspensao is not None:
            suspensao = timezone.datetime.strptime(suspensao, '%Y-%m-%d').date()
            if suspensao >= hoje:
                raise serializers.ValidationError('Você está suspenso')

        if Emprestimo.objects.filter(
            usuario_id=usuario_id,
            data_devolucao=None,
            data_limite__lt=hoje
        ).exists():
            raise serializers.ValidationError('Você tem empréstimos atrasados')

    def validar_emprestimos(self, livro_id):
        if Emprestimo.objects.filter(
            livro_id=livro_id,
            usuario_id=self.context['request'].user['_id'],
            data_devolucao=None
        ).exists():
            raise serializers.ValidationError('Você já possui um exemplar desse livro emprestado')

    def validar_reservas(self, livro_id):
        hoje = timezone.now().date()
        usuario_id = self.context['request'].user['_id']
        
        if Reserva.objects.filter(
            Q(disponibilidade_retirada=None) | Q(disponibilidade_retirada__gte=hoje),
            usuario_id=usuario_id,
            livro_id=livro_id,
            cancelada=False,
            emprestimo_id=None
        ).exists():
            raise serializers.ValidationError('Você tem uma reserva vigente para este livro')

    def validar_livro(self, livro_id):
        try:
            r = requests.get(CATALOGO_SERVICE_URL + '/livros/' + livro_id)
            if not r.ok:
                raise serializers.ValidationError('Livro não encontrado')

            hoje = timezone.now().date()
            livro = r.json()
            exemplares_disponiveis = livro['exemplares_disponiveis']

            if exemplares_disponiveis > 0:
                if Reserva.objects.filter(
                    Q(disponibilidade_retirada=None) | Q(disponibilidade_retirada__gte=hoje),
                    livro_id=livro_id,
                    cancelada=False,
                    emprestimo_id=None
                ).count() < exemplares_disponiveis:
                    raise serializers.ValidationError('Há exemplares desse livro disponíveis')
        
        except serializers.ValidationError as e:
            raise e

        except:
            raise serializers.ValidationError('Serviço demorou muito a responder')

    def create(self, data):
        return Reserva.objects.create(
            livro_id=data['livro_id'],
            usuario_id=self.context['request'].user['_id']
        )

    class Meta:
        model = Reserva
        fields = [
            'livro_id'
        ]
