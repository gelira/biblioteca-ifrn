import os

from .base import BaseProxyView

AQUISICAO_SERVICE_URL = os.getenv('AQUISICAO_SERVICE_URL')

class AquisicaoProxyView(BaseProxyView):
    upstream = AQUISICAO_SERVICE_URL
