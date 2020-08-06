from rest_framework import serializers

from ..models import Perfil

class PerfilSerializer(serializers.ModelSerializer):
    def assegurarPerfilPadraoUnico(self, data):
        if Perfil.objects.filter(padrao=True).count() == 0:
            data['padrao'] = True
        elif data['padrao']:
            Perfil.objects.filter(padrao=True).update(padrao=False)
        return data

    def create(self, data):
        data = self.assegurarPerfilPadraoUnico(data)
        return super().create(data)

    def update(self, instance, data):
        data = self.assegurarPerfilPadraoUnico(data)
        return super().update(instance, data) 

    class Meta:
        model = Perfil
        fields = '__all__'
