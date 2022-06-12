import os
import requests
from django.utils import timezone

from .. import exceptions
from ..models import Emprestimo

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')
AUTENTICACAO_TIMEOUT = int(os.getenv('AUTENTICACAO_TIMEOUT'))

class AutenticacaoService:
    url_token = AUTENTICACAO_SERVICE_URL + '/token'
    url_informacoes_usuario = AUTENTICACAO_SERVICE_URL + '/informacoes'
    url_consulta_usuario = AUTENTICACAO_SERVICE_URL + '/consulta'
    url_suspensoes = AUTENTICACAO_SERVICE_URL + '/suspensoes'
    url_abono_suspensoes = AUTENTICACAO_SERVICE_URL + '/abono-suspensoes'

    @classmethod
    def autenticar_usuario(cls, matricula, senha):
        data_token = cls.login_suap(matricula, senha)
        return cls.informacoes_usuario(token=data_token['token'])

    @classmethod
    def login_suap(cls, username, password):
        response = cls.dispatch({
            'method': 'POST',
            'url': cls.url_token,
            'json': {
                'username': username,
                'password': password
            }
        })

        return response.json()

    @classmethod
    def informacoes_usuario(cls, usuario_id=None, token=None, save_cache=False):
        if not usuario_id and not token:
            raise Exception('Uma das opções deve ser definida: usuario_id ou token')
        
        options = { 
            'method': 'GET', 
            'url': cls.url_informacoes_usuario,
        }

        if usuario_id:
            options['headers'] = { 
                'X-Usuario-Id': usuario_id, 
            }
 
        else:
            options['headers'] = {
                'Authorization': f'JWT {token}',
            }

        if save_cache:
            options['params'] = {
                'save_cache': True
            }

        response = cls.dispatch(options)

        return response.json()

    @classmethod
    def consulta_usuario(cls, usuario_id):
        response = cls.dispatch({
            'method': 'GET',
            'url': cls.url_consulta_usuario,
            'params': {
                'id': usuario_id
            }
        })

        return response.json()

    @classmethod
    def suspensoes(cls, suspensoes):
        cls.dispatch({
            'method': 'POST',
            'url': cls.url_suspensoes,
            'json': suspensoes
        })
    
    @classmethod
    def abono_suspensoes(cls, suspensoes):
        cls.dispatch({
            'method': 'POST',
            'url': cls.url_abono_suspensoes,
            'json': suspensoes
        })

    @classmethod
    def check_usuario_suspenso(cls, usuario_id, suspensao, hoje=None):
        if not hoje:
            hoje = timezone.localdate()

        if suspensao is not None:
            suspensao = timezone.datetime.strptime(suspensao, '%Y-%m-%d').date()
            if suspensao >= hoje:
                raise exceptions.UsuarioSuspenso

        if Emprestimo.objects.filter(
            usuario_id=usuario_id,
            data_devolucao=None,
            data_limite__lt=hoje
        ).exists():
            raise exceptions.EmprestimosAtrasados

    @classmethod
    def dispatch(self, options):
        method = options.pop('method')
        url = options.pop('url')
        options['timeout'] = AUTENTICACAO_TIMEOUT
        
        try:
            response = requests.request(method, url, **options)
            response.raise_for_status()
            return response

        except requests.exceptions.HTTPError:
            raise exceptions.ServiceUnauthorized
        
        except requests.exceptions.ConnectTimeout:
            raise exceptions.ServiceTimeOut
        
        except requests.exceptions.ConnectionError:
            raise exceptions.ServiceUnavailable
