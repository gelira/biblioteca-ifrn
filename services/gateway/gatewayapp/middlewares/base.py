ALLOW_URLS = [
    '/autenticacao/token',
    '/autenticacao/verificar',
    '/catalogo/media',
]

class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.allow_url(request):
            return self.get_response(request)
        return self.process_request(request)

    def allow_url(self, request):
        for url in ALLOW_URLS:
            if request.path.startswith(url):
                return True
        return False

    def process_request(self, request):
        raise NotImplemented
