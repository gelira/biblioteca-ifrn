import os
import requests
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from ..models import Reserva

CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')

class ReservaCreateSerializer(serializers.ModelSerializer):
    def validate_livro_id(self, value):
        livro_id = str(value)
        self.validar_reservas(livro_id)
        self.validar_livro(livro_id)
        return value

    def validar_reservas(self, livro_id):
        agora = timezone.now()
        usuario_id = self.context['request'].user['_id']
        
        if Reserva.objects.filter(
            Q(disponibilidade_retirada=None) | Q(disponibilidade_retirada__gt=agora),
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

            agora = timezone.now()
            livro = r.json()
            exemplares_disponiveis = livro['exemplares_disponiveis']

            if exemplares_disponiveis > 0:
                if Reserva.objects.filter(
                    Q(disponibilidade_retirada=None) | Q(disponibilidade_retirada__gt=agora),
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
