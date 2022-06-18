from django.utils import timezone

from ..models import Data

class FeriadoService:
    @classmethod
    def create_dias_feriado(cls, feriado, data_inicio, data_fim):
        while data_inicio <= data_fim:
            Data.objects.create(
                feriado=feriado,
                dia=data_inicio.day,
                mes=data_inicio.month,
                ano=data_inicio.year
            )
            data_inicio = data_inicio + timezone.timedelta(days=1)    

    @classmethod
    def check_date_exists(cls, date):
        return Data.objects.filter(
            dia=date.day, 
            mes=date.month, 
            ano=date.year
        ).exists()

    @classmethod
    def check_emprestimo_exemplar_referencia(cls):
        hoje = timezone.localdate()

        if hoje.weekday() == 4:
            return True

        amanha = hoje + timezone.timedelta(days=1)
        
        return cls.check_date_exists(amanha)

    @classmethod
    def calcular_data_limite(cls, max_dias=None):
        hoje = timezone.localdate()

        if max_dias is not None:
            hoje = hoje + timezone.timedelta(days=max_dias)
        
        while True:
            if hoje.weekday() < 5:
                if not cls.check_date_exists(hoje):
                    return hoje

            hoje = hoje + timezone.timedelta(days=1)
