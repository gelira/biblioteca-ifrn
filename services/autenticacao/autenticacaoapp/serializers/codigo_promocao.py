import uuid
from django.utils import timezone
from django.db import transaction
from rest_framework import serializers

from ..models import (
    CodigoPromocao, 
    Usuario
)
from ..cliente_redis import ClienteRedis

class CodigoPromocaoCreateSerializer(serializers.ModelSerializer):
    def create_codigo(self):
        while True:
            codigo = str(uuid.uuid4())[:6].upper()
            if not CodigoPromocao.objects.filter(
                codigo=codigo,
                validade__gte=timezone.now(),
                bolsista=None
            ).exists():
                return codigo

    def get_usuario(self):
        return Usuario.objects.get(user=self.context['request'].user)

    def create(self, data):
        codigo = self.create_codigo()
        usuario = self.get_usuario()
        validade = timezone.now() + timezone.timedelta(minutes=5)

        return CodigoPromocao.objects.create(
            usuario=usuario,
            codigo=codigo,
            validade=validade
        )

    class Meta:
        model = CodigoPromocao
        fields = [
            'codigo'
        ]
        extra_kwargs = {
            'codigo': {
                'read_only': True
            }
        }

class UtilizarCodigoPromocaoSerializer(serializers.Serializer):
    codigo = serializers.CharField(
        min_length=1,
        max_length=20
    )

    def validate(self, data):
        codigo = CodigoPromocao.objects.filter(
            codigo=data['codigo'],
            validade__gte=timezone.now()
        ).first()
        
        if codigo is None:
            raise serializers.ValidationError('Código inválido')
        
        data['codigo'] = codigo
        return data

    def create(self, data):
        with transaction.atomic():
            usuario = self.context['request'].user.usuario
            _id = str(usuario._id)
            codigo = data['codigo']

            codigo.codigo_utilizado = codigo.codigo
            codigo.codigo = ''
            codigo.bolsista = usuario
            codigo.save()

            cr = ClienteRedis()
            u = cr.get(_id)

            for p in ['emprestimo.fazer', 'emprestimo.receber_devolucao']:
                if p not in u['lista_permissoes']:
                    u['lista_permissoes'].append(p)
            
            cr.store(_id, u, True)

            return {}
