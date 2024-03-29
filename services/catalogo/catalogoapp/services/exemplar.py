import random, string
from django.db.utils import IntegrityError
from django.utils.timezone import localtime

from .. import exceptions
from ..models import Exemplar

class ExemplarService:
    charset = string.ascii_uppercase + string.digits

    @classmethod
    def gerar_codigo(cls):
        chars = [random.choice(cls.charset) for _ in range(8)]
        return ''.join(chars)

    @classmethod
    def create_exemplar(cls, livro, referencia):
        while True:
            try:
                return Exemplar.objects.create(
                    livro=livro,
                    referencia=referencia,
                    codigo=cls.gerar_codigo()
                )

            except IntegrityError:
                continue

    @classmethod
    def set_disponibilidade_exemplares(cls, codigos, disponivel):
        Exemplar.objects.filter(codigo__in=codigos).update(
            disponivel=disponivel,
            updated=localtime()
        )

    @classmethod
    def exemplares_emprestados(cls, codigos):
        cls.set_disponibilidade_exemplares(codigos, False)

    @classmethod
    def exemplares_devolvidos(cls, codigos):
        cls.set_disponibilidade_exemplares(codigos, True)

    @classmethod
    def consulta_codigo_exemplar(cls, codigo):
        e = Exemplar.objects.filter(codigo=codigo).first()
        
        if not e:
            raise exceptions.ExemplarNotFound

        return e
