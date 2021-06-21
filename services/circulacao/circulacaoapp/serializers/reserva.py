import os
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from ..services import CatalogoService 
from ..models import (
    Reserva,
    Emprestimo
)
from ..utils import calcular_data_limite
from ..tasks import (
    enviar_reservas_disponiveis
)

PROJECT_NAME = os.getenv('PROJECT_NAME')

class ReservaCreateSerializer(serializers.ModelSerializer):
    def validate_livro_id(self, value):
        livro_id = str(value)
        self.validar_usuario_suspenso()
        self.validar_emprestimos(livro_id)
        self.validar_reservas(livro_id)
        self.validar_livro(livro_id)
        self.validar_quantidade_reservas_emprestimos()
        return value

    def validar_usuario_suspenso(self):
        usuario_id = self.context['request'].user['_id']
        suspensao = self.context['request'].user['suspensao']
        hoje = timezone.localdate()

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
        hoje = timezone.localdate()
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
            hoje = timezone.localdate()
            livro = CatalogoService.busca_livro(livro_id)
            
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

    def validar_quantidade_reservas_emprestimos(self):
        usuario_id = self.context['request'].user['_id']
        hoje = timezone.localdate()

        emprestimos = Emprestimo.objects.filter(
            usuario_id=usuario_id,
            data_devolucao=None
        ).count()
        reservas = Reserva.objects.filter(
            Q(disponibilidade_retirada=None) | Q(disponibilidade_retirada__gte=hoje),
            usuario_id=usuario_id,
            cancelada=False,
            emprestimo_id=None
        ).count()

        if emprestimos + reservas + 1 > self.context['request'].user['perfil']['max_livros']:
            raise serializers.ValidationError('Seus empréstimos + reservas estão no limite')

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

class CancelarReservaSerializer(serializers.Serializer):
    reserva = serializers.UUIDField()

    def validate_reserva(self, value):
        reserva = Reserva.objects.filter(
            _id=value,
            usuario_id=self.context['request'].user['_id']
        ).first()

        if reserva is None:
            raise serializers.ValidationError('Reserva não encontrada')

        if reserva.cancelada:
            raise serializers.ValidationError('Reserva já cancelada')

        if reserva.emprestimo_id is not None:
            raise serializers.ValidationError('Reserva já atendida')

        return reserva

    def create(self, data):
        proxima_reserva = None

        with transaction.atomic():
            reserva = data['reserva']
            reserva.cancelada = True
            reserva.save()

            if reserva.disponibilidade_retirada is not None:
                proxima_reserva = Reserva.objects.filter(
                    disponibilidade_retirada=None,
                    livro_id=reserva.livro_id,
                    emprestimo_id=None,
                    cancelada=False
                ).first()

                if proxima_reserva is not None:
                    proxima_reserva.disponibilidade_retirada = calcular_data_limite(1)
                    proxima_reserva.save()

        if proxima_reserva:
            agora = timezone.localtime()
            comprovante = {
                'usuario_id': str(proxima_reserva.usuario_id),
                'livro_id': str(proxima_reserva.livro_id),
                'data': agora.strftime('%d/%m/%Y'),
                'hora': agora.strftime('%H:%M:%S'),
                'data_limite': proxima_reserva.disponibilidade_retirada.strftime('%d/%m/%Y')
            }
            enviar_reservas_disponiveis.apply_async([[comprovante]], queue=PROJECT_NAME)

        return {}
