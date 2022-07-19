from ..models import Perfil

class PerfilService:
    @classmethod
    def assegurar_perfil_padrao_unico(cls, criando_perfil_padrao):
        if Perfil.objects.filter(padrao=True).count() == 0:
            return True
        
        if criando_perfil_padrao:
            Perfil.objects.filter(padrao=True).update(padrao=False)

        return criando_perfil_padrao
