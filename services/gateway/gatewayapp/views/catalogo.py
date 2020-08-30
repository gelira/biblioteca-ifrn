import os

from .base import BaseProxyView

CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')

class CatalogoProxyView(BaseProxyView):
    upstream = CATALOGO_SERVICE_URL
