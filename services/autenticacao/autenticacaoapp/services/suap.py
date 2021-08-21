import os
import requests

SUAP_URL_AUTENTICACAO = os.getenv('SUAP_URL_AUTENTICACAO')
SUAP_URL_DADOS = os.getenv('SUAP_URL_DADOS')
SUAP_TIMEOUT = int(os.getenv('SUAP_TIMEOUT'))

class SuapTimeOut(Exception):
    pass

class SuapUnauthorized(Exception):
    pass

class SuapUnavailable(Exception):
    pass

class SuapService:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None

    def autenticar(self):
        retorno = self.dispatch({
            'method': 'POST',
            'url': SUAP_URL_AUTENTICACAO,
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
            'url': SUAP_URL_DADOS,
            'headers': {
                'Authorization': f'JWT {self.token}',
                'Accept': 'application/json'
            }
        })

    def dispatch(self, options):
        method = options.pop('method')
        url = options.pop('url')
        options['timeout'] = SUAP_TIMEOUT
        
        try:
            response = requests.request(method, url, **options)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError:
            raise SuapUnauthorized
        
        except requests.exceptions.ConnectTimeout:
            raise SuapTimeOut
        
        except requests.exceptions.ConnectionError:
            raise SuapUnavailable
