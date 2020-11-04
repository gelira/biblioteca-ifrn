import os
import requests
from rest_framework import serializers

from ..models import Reserva

CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')

class ReservaCreateSerializer(serializers.ModelSerializer):
    def validate_livro_id(self, value):
        self.validar_livro(str(value))
        return value

    def validar_livro(self, livro_id):
        try:
            r = requests.get(CATALOGO_SERVICE_URL + '/livros/' + livro_id)
            if not r.ok:
                raise serializers.ValidationError('Livro não encontrado')

            livro = r.json()
            if livro['exemplares_disponiveis'] > 0:
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
