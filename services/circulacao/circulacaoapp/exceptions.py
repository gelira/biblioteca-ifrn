from rest_framework.exceptions import APIException
from rest_framework import status

class ServiceUnauthorized(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Acesso não autorizado'
    default_code = 'unauthorized'

class ServiceBadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Ocorreu algum problema ao acessar esse recurso'
    default_code = 'bad_request'

class ServiceTimeOut(APIException):
    status_code = status.HTTP_504_GATEWAY_TIMEOUT
    default_detail = 'Serviço demorou muito a responder'
    default_code = 'service_timeout'

class ServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Serviço indisponível'
    default_code = 'service_unavailable'

class UsuarioSuspenso(APIException):
    default_detail = 'Usuário está suspenso'

class EmprestimosAtrasados(APIException):
    default_detail = 'Usuário tem empréstimos atrasados'

class LivroEmprestadoUsuario(APIException):
    default_detail = 'Usuário já possui um exemplar desse livro emprestado'

class ReservaVigente(APIException):
    default_detail = 'Usuário tem uma reserva vigente para este livro'

class ExemplaresDisponiveis(APIException):
    default_detail = 'Há exemplares desse livro disponíveis'

class LimiteEmprestimosReservas(APIException):
    default_detail = 'Os empréstimos + reservas do usuário estão no limite'

class LimiteEmprestimos(APIException):
    default_detail = 'O limite de livros para o usuário foi atingido'

class ReservaNotFound(APIException):
    default_detail = 'Reserva não encontrada'

class ReservaCancelada(APIException):
    default_detail = 'Reserva já cancelada'

class ReservaAtendida(APIException):
    default_detail = 'Reserva já atendida'

class ExemplarLivroEmprestadoUsuario(APIException):
    default_detail = 'Usuário não pode pegar dois exemplares do mesmo livro'
