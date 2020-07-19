import requests

URL_AUTENTICACAO = 'https://suap.ifrn.edu.br/api/v2/autenticacao/token/'
URL_DADOS = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/'

class SUAP:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None

    def autenticar(self):
        try:
            response = requests.post(URL_AUTENTICACAO, json={
                'username': self.username,
                'password': self.password
            })
            retorno = { 'ok': response.status_code == 200 }
            if retorno['ok']:
                json = response.json()
                self.token = json['token']
                retorno.update(json)
            return retorno
        except:
            return None

    def dados_usuario(self):
        if self.token is None:
            raise ValueError('Não foi gerado token')
        try:
            response = requests.get(URL_DADOS, headers={
                'Authorization': 'JWT {}'.format(self.token)
            })
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
