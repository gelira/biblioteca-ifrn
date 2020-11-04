import os
import requests
from rest_framework import serializers

from ..models import Reserva

CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')

class ReservaCreateSerializer(serializers.ModelSerializer):
    def create(self, data):
        return Reserva.objects.create(
            livro_id=data['livro_id'],
            usuario_id=self.context['request'].user['_id']
        )
    
    def validate_livro_id(self, value):
        try:
            r = requests.get(CATALOGO_SERVICE_URL + '/livros/' + str(value))
            if not r.ok:
                raise serializers.ValidationError('Livro não encontrado')

            livro = r.json()
            if livro['exemplares_disponiveis'] > 0:
                raise serializers.ValidationError('Há exemplares desse livro disponíveis')

            return value
        
        except serializers.ValidationError as e:
            raise e

        except:
            raise serializers.ValidationError('Serviço demorou muito a responder')

    class Meta:
        model = Reserva
        fields = [
            'livro_id'
        ]
