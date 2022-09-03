import uuid
from django.utils import timezone
from django.db import transaction

from .. import exceptions
from ..models import CodigoPromocao, Usuario
from ..cliente_redis import ClienteRedis

class PromocaoService:
    @classmethod
    def generate_codigo_promocao(self):
        while True:
            upper_uuid = str(uuid.uuid4()).upper()
            codigo = upper_uuid[:6]

            if not CodigoPromocao.objects.filter(
                codigo=codigo,
                validade__gte=timezone.localtime(),
                bolsista=None
            ).exists():
                return codigo

    @classmethod
    def create_codigo_promocao(cls, user):
        usuario = Usuario.objects.filter(user=user).first()
        if not usuario:
            raise exceptions.UserNotFound

        codigo = cls.generate_codigo_promocao()

        validade = timezone.localtime() + timezone.timedelta(minutes=5)

        return CodigoPromocao.objects.create(
            usuario=usuario,
            codigo=codigo,
            validade=validade
        )

    @classmethod
    def validate_codigo_promocao(cls, codigo):
        codigo_promocao = CodigoPromocao.objects.filter(
            codigo=codigo,
            validade__gte=timezone.localtime()
        ).first()
        
        if not codigo_promocao:
            raise exceptions.InvalidCodigoPromocao

        if codigo_promocao.bolsista_id is not None:
            raise exceptions.InvalidCodigoPromocao

        return codigo_promocao

    @classmethod
    def use_codigo_promocao(cls, usuario, codigo_promocao):
        with transaction.atomic():
            _id = str(usuario._id)

            codigo_promocao.bolsista = usuario
            codigo_promocao.save()

            cr = ClienteRedis()
            u = cr.get(_id)

            for p in ['emprestimo.fazer', 'emprestimo.receber_devolucao']:
                if p not in u['lista_permissoes']:
                    u['lista_permissoes'].append(p)
            
            cr.store(_id, u, update=True)
            