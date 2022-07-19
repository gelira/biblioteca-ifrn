from rest_framework.exceptions import APIException
from rest_framework import status

class ServiceUnauthorized(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Acesso não autorizado'
    default_code = 'unauthorized'

class ServiceTimeOut(APIException):
    status_code = status.HTTP_504_GATEWAY_TIMEOUT
    default_detail = 'Serviço demorou muito a responder'
    default_code = 'service_timeout'

class ServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Serviço indisponível'
    default_code = 'service_unavailable'

class LivroNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Livro não encontrado'
    default_code = 'livro_not_found'

class ExemplarNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Exemplar não encontrado'
    default_code = 'exemplar_not_found'
