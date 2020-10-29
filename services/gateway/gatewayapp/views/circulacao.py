import os

from .base import BaseProxyView

CIRCULACAO_SERVICE_URL = os.getenv('CIRCULACAO_SERVICE_URL')

class CirculacaoProxyView(BaseProxyView):
    upstream = CIRCULACAO_SERVICE_URL
