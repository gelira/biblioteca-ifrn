from rest_framework import permissions

from ..cliente_redis import ClienteRedis

class BasePermission(permissions.BasePermission):
    def __init__(self):
        self.cliente_redis = ClienteRedis()
