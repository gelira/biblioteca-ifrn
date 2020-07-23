import requests

from .exceptions import SUAPTimeOut, SUAPUnauthorized, SUAPUnavailable

URL_AUTENTICACAO = 'https://suap.ifrn.edu.br/api/v2/autenticacao/token/'
URL_DADOS = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/'
TIMEOUT = 5

class SUAP:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None

    def autenticar(self):
        retorno = self.dispatch({
            'method': 'POST',
            'url': URL_AUTENTICACAO,
            'json': {
                'username': self.username,
                'password': self.password
            }
        })
        self.token = retorno['token']
        return retorno

    def dados_usuario(self):
        if self.token is None:
            raise ValueError('Não foi gerado token')
        return self.dispatch({
            'method': 'GET',
            'url': URL_DADOS,
            'headers': {
                'Authorization': 'JWT {}'.format(self.token),
                'Accept': 'application/json'
            }
        })

    def dispatch(self, options):
        method = options.pop('method')
        url = options.pop('url')
        options['timeout'] = TIMEOUT
        
        try:
            response = requests.request(method, url, **options)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError:
            raise SUAPUnauthorized
        
        except requests.exceptions.ConnectTimeout:
            raise SUAPTimeOut
        
        except requests.exceptions.ConnectionError:
            raise SUAPUnavailable
