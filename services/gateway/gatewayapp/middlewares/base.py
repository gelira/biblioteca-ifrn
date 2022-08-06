from django.http.response import JsonResponse
from rest_framework.exceptions import APIException

ALLOW_URLS = [
    '/autenticacao/token',
]

class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.allow_url(request):
            return self.get_response(request)

        try:
            return self.process_request(request)
        
        except APIException as e:
            return JsonResponse(
                data={
                    'message': e.default_detail,
                    'code': e.default_code,
                }, 
                status=e.default_code
            )

    def allow_url(self, request):
        for url in ALLOW_URLS:
            if request.path.startswith(url):
                return True
        return False

    def process_request(self, request):
        raise NotImplemented
