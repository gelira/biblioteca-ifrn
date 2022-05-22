from rest_framework import status
from rest_framework.exceptions import APIException

class SuapTimeOut(APIException):
    status_code = status.HTTP_504_GATEWAY_TIMEOUT
    default_detail = 'SUAP demorou muito a responder'
    default_code = 'suap_timeout'

class SuapUnauthorized(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Credenciais inválidas para autenticação com o SUAP'
    default_code = 'suap_unauthorized'

class SuapUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'SUAP indisponível no momento'
    default_code = 'suap_unavailable'

class InvalidCredentials(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Credenciais inválidas'
    default_code = 'invalid_credentials'

class InvalidToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Token inválido'
    default_code = 'invalid_token'

class InvalidUUID(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'UUID inválido'
    default_code = 'invalid_uuid'

class UserNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Usuário não encontrado'
    default_code = 'user_not_found'

class InvalidCodigoPromocao(Exception):
    pass
