import json
from redis import Redis

class ClienteRedis:
    def __init__(self):
        self.con = Redis(host='172.25.0.11', db=10)

    def store(self, chave, valor):
        if not isinstance(valor, str):
            valor = json.dumps(valor)
        self.con.set(chave, valor, ex=4*60*60)

    def exist(self, chave):
        return self.con.exists(chave) > 0

    def get(self, chave):
        valor = self.con.get(chave)
        if valor is None:
            return None
        return json.loads(valor)
