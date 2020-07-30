from rest_framework_simplejwt.tokens import AccessToken

class AcessoToken(AccessToken):
    @classmethod
    def for_user(cls, user):
        return super().for_user(user.usuario)
