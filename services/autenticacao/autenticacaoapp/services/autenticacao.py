import uuid
from django.contrib.auth import get_user_model, authenticate

from .. import exceptions
from ..models import Usuario, Perfil
from .suap import SuapService
from .token import TokenService
from .notificacao import NotificacaoService

User = get_user_model()

class AutenticacaoService:
    @classmethod
    def login_suap(cls, username, password):
        suap = SuapService(username, password)
        suap.autenticar()
        
        user = cls.get_or_save_usuario(suap)
        token = TokenService.gerar_token(user)

        return {
            'token': token
        }

    @classmethod
    def login_local(cls, username, password):
        user = authenticate(username=username, password=password)
        if not user:
            raise exceptions.InvalidCredentials

        if user.usuario.vinculo == 'service':
            raise exceptions.InvalidCredentials

        token = TokenService.gerar_token(user)

        return {
            'token': token
        }

    @classmethod
    def get_or_save_usuario(cls, suap):
        user = User.objects.filter(**{ 
            User.USERNAME_FIELD: suap.username 
        }).first()
        
        if user is None:
            user = cls.save_usuario(suap)

        return user
        
    @classmethod
    def save_usuario(cls, suap):    
        dados = suap.dados_usuario()

        nome = dados['nome_usual']
        matricula = dados['matricula']
        email_institucional = dados['email']
        
        user = User.objects.create_user(matricula, password=matricula)
        u = Usuario.objects.create(
            user=user,
            nome=nome,
            nome_completo=dados['vinculo']['nome'],
            email_institucional=email_institucional,
            vinculo=dados['tipo_vinculo'].lower(),
            url_foto=dados['url_foto_150x200']
        )

        perfil = Perfil.objects.filter(padrao=True).first()
        if perfil is not None:
            u.perfil = perfil
            u.save()

        NotificacaoService.salvar_contato(
            str(u._id),
            {
                'nome': nome,
                'matricula': matricula,
                'email_institucional': email_institucional,
            }
        )

        return user

    @classmethod
    def informacoes_usuario(cls, usuario_id):
        try:
            uuid.UUID(usuario_id)
        except:
            raise exceptions.InvalidUUID

        usuario = Usuario.objects.filter(_id=usuario_id).first()
        if not usuario:
            raise exceptions.UserNotFound

        return usuario

    @classmethod
    def consulta_usuario(cls, usuario_id, matricula=None):
        if matricula:
            user = User.objects.filter(username=matricula).first()
            if not user:
                raise exceptions.UserNotFound
            
            return user.usuario

        try:
            uuid.UUID(usuario_id)
        except:
            raise exceptions.InvalidUUID

        usuario = Usuario.objects.filter(_id=usuario_id).first()
        if not usuario:
            raise exceptions.UserNotFound

        return usuario
