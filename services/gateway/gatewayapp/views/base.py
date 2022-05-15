from django.http.response import JsonResponse
from revproxy.views import ProxyView
from urllib3.exceptions import MaxRetryError

class BaseProxyView(ProxyView):
    def dispatch(self, request, path):
        try:
            return super().dispatch(request, path)

        except MaxRetryError:
            return JsonResponse({ 
                'message': 'Serviço indisponível',
                'code': 'service_unavailable' 
            }, status=503)

    def get_request_headers(self):
        headers = super().get_request_headers()
        headers.pop('Authorization', None)

        usuario_id = self.request.META.get('_id')

        if usuario_id is not None:
            headers['X-Usuario-Id'] = usuario_id

        return headers
