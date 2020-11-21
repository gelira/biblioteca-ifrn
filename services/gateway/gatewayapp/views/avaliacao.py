import os

from .base import BaseProxyView

AVALIACAO_SERVICE_URL = os.getenv('AVALIACAO_SERVICE_URL')

class AvaliacaoProxyView(BaseProxyView):
    upstream = AVALIACAO_SERVICE_URL
