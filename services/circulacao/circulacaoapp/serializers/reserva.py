from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from ..services import (
    CatalogoService,
    ReservaService
) 
from ..models import (
    Reserva,
    Emprestimo
)

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
        livros = []

        with transaction.atomic():
            reserva = data['reserva']
            reserva.cancelada = True
            reserva.save()

            if reserva.disponibilidade_retirada is not None:
                livros.append(str(reserva.livro_id))

        if livros: 
            ReservaService.call_proximas_reservas(livros)

        return {}
