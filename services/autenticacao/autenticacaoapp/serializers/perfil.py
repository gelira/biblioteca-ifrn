from rest_framework import serializers

from ..models import Perfil

class PerfilSerializer(serializers.ModelSerializer):
    def assegurar_perfil_padrao_unico(self, data):
        if Perfil.objects.filter(padrao=True).count() == 0:
            data['padrao'] = True
        elif data['padrao']:
            Perfil.objects.filter(padrao=True).update(padrao=False)
        return data

    def create(self, data):
        data = self.assegurar_perfil_padrao_unico(data)
        return super().create(data)

    def update(self, instance, data):
        data = self.assegurar_perfil_padrao_unico(data)
        return super().update(instance, data) 

    class Meta:
        model = Perfil
        fields = '__all__'
