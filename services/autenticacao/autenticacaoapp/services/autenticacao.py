import uuid
from django.contrib.auth import get_user_model

from ..models import Usuario, Perfil
from ..serializers import UsuarioSerializer, UsuarioConsultaSerializer
from .suap import SuapService, SuapUnauthorized, SuapTimeOut, SuapUnavailable
from .token import TokenService

User = get_user_model()

class AutenticacaoService:
    @classmethod
    def login_suap(cls, username, password):
        suap = SuapService(username, password)

        try:
            suap.autenticar()

        except SuapUnauthorized:
            raise Exception({
                'error': {
                    'detail': 'Credenciais inválidas',
                },
                'status': 401
            })

        except SuapTimeOut:
            raise Exception({
                'error': {
                    'detail': 'Serviço demorou demais para responder'
                },
                'status': 408
            })

        except SuapUnavailable:
            raise Exception({
                'error': {
                    'detail': 'Serviço indisponível'
                },
                'status': 503
            })

        except Exception as e:
            raise Exception({
                'error': {
                    'detail': str(e)
                }
            })
        
        user = cls.get_or_save_usuario(suap)
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
        dados = None
        
        try:
            dados = suap.dados_usuario()
        
        except SuapUnauthorized:
            raise Exception({
                'error': {
                    'detail': 'Credenciais inválidas'
                },
                'status': 401
            })

        except SuapTimeOut:
            raise Exception({
                'error': {
                    'detail': 'Serviço demorou demais para responder'
                },
                'status': 408
            })

        except SuapUnavailable:
            raise Exception({
                'error': {
                    'detail': 'Serviço indisponível'
                },
                'status': 503
            })

        matricula = dados['matricula']
        
        user = User.objects.create_user(matricula, password=matricula)
        u = Usuario.objects.create(
            user=user,
            nome=dados['nome_usual'],
            nome_completo=dados['vinculo']['nome'],
            email_institucional=dados['email'],
            vinculo=dados['tipo_vinculo'].lower(),
            url_foto=dados['url_foto_150x200']
        )

        perfil = Perfil.objects.filter(padrao=True).first()
        if perfil is not None:
            u.perfil = perfil
            u.save()

        return user

    @classmethod
    def informacoes_usuario(cls, usuario_id):
        try:
            uuid.UUID(usuario_id)
        except:
            raise Exception({
                'error': {
                    'detail': 'UUID inválido'
                },
                'status': 400
            })

        usuario = Usuario.objects.filter(_id=usuario_id).first()
        if not usuario:
            raise Exception({
                'error': {
                    'detail': 'Usuário não encontrado'
                },
                'status': 404
            })

        ser = UsuarioSerializer(usuario)
        return ser.data

    @classmethod
    def consulta_usuario(cls, usuario_id, matricula=None):
        usuario = None
        
        if matricula:
            user = User.objects.filter(username=matricula).first()
            if not user:
                raise Exception({
                    'error': {
                        'detail': 'Usuário não encontrado'
                    },
                    'status': 404
                })
            
            usuario = user.usuario

        else:
            try:
                uuid.UUID(usuario_id)
            except:
                raise Exception({
                    'error': {
                        'detail': 'UUID inválido'
                    },
                    'status': 400
                })

            usuario = Usuario.objects.filter(_id=usuario_id).first()
            if not usuario:
                raise Exception({
                    'error': {
                        'detail': 'Usuário não encontrado'
                    },
                    'status': 404
                })

        ser = UsuarioConsultaSerializer(usuario)
        return ser.data
