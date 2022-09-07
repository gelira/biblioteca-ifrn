import os
import json
from redis import Redis
from circuitbreaker import circuit

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_DB = int(os.getenv('REDIS_DB'))

class ClienteRedis:
    def __init__(self):
        self.con = Redis(
            host=REDIS_HOST, 
            db=REDIS_DB,
            socket_connect_timeout=2,
            socket_timeout=2
        )

    @circuit(failure_threshold = 1, recovery_timeout = 60)
    def store(self, chave, valor, update=False):
        if not isinstance(valor, str):
            valor = json.dumps(valor)
        
        if update:
            self.con.set(chave, valor, keepttl=True)
        else:
            self.con.set(chave, valor, ex=4*60*60)

    @circuit(failure_threshold = 1, recovery_timeout = 60)
    def exist(self, chave):
        return self.con.exists(chave) > 0

    @circuit(failure_threshold = 1, recovery_timeout = 60)
    def get(self, chave):
        valor = self.con.get(chave)
        if valor is None:
            return None
        return json.loads(valor)
