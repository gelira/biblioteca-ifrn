from django.utils import timezone

from ..models import Data

def calcular_data_limite(max_dias=None):
    hoje = timezone.localdate()

    if max_dias is not None:
        hoje = hoje + timezone.timedelta(days=max_dias)
    
    while True:
        if hoje.weekday() < 5:
            if not Data.objects.filter(dia=hoje.day, mes=hoje.month, ano=hoje.year).exists():
                return hoje
        hoje = hoje + timezone.timedelta(days=1)
