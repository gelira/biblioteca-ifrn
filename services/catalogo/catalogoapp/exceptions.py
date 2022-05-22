from rest_framework.exceptions import APIException
from rest_framework import status

class LivroNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Livro não encontrado'
    default_code = 'livro_not_found'

class ExemplarNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Exemplar não encontrado'
    default_code = 'exemplar_not_found'
