from django.utils.timezone import localtime

from ..models import Exemplar

class ExemplarService:
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
            raise Exception({
                'error': {
                    'detail': 'Exemplar não encontrado'
                },
                'status': 404
            })

        from ..serializers import ExemplarConsultaSerializer

        ser = ExemplarConsultaSerializer(e)
        return ser.data
