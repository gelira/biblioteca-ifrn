from rest_framework import serializers
from rest_framework.exceptions import APIException

from ..models import Emprestimo
from ..services import (
    AutenticacaoService,
    EmprestimoService,
    DevolucaoService
)

class EmprestimoRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprestimo
        exclude = [
            'id',
            'usuario_id'
        ]

class EmprestimoCreateSerializer(serializers.Serializer):
    matricula = serializers.CharField()
    senha = serializers.CharField()
    codigos = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )
    
    def validate(self, data):
        matricula = data['matricula']
        senha = data['senha']
        codigos = data['codigos']

        try:
            usuario = self.validar_usuario(matricula, senha)
            usuario_id = usuario['_id']
            suspensao = usuario['suspensao']
            max_livros = usuario['perfil']['max_livros']

            AutenticacaoService.check_usuario_suspenso(usuario_id, suspensao)

            livros_emprestados_id = EmprestimoService.check_emprestimos_usuario(
                usuario_id, 
                max_livros, 
                len(codigos)
            )

            exemplares, reservas = EmprestimoService.check_codigos(
                usuario_id, 
                codigos, 
                livros_emprestados_id
            )

            data['usuario'] = usuario
            data['exemplares'] = exemplares
            data['reservas'] = reservas
            
            return data

        except APIException as e:
            raise serializers.ValidationError(str(e))

    def create(self, data):
        exemplares = data['exemplares']
        codigos = data['codigos']
        reservas = data['reservas']
        usuario = data['usuario']
        atendente_id = self.context['request'].user['_id']

        return EmprestimoService.create_emprestimos(
            exemplares,
            codigos,
            reservas,
            usuario,
            atendente_id
        )

    def validate_codigos(self, value):
        return list(set(value))

    def validar_usuario(self, matricula, senha):
        try:
            return AutenticacaoService.autenticar_usuario(matricula, senha)

        except APIException:
            raise serializers.ValidationError('Não foi possível validar as credenciais do usuário')

class DevolucaoEmprestimosSerializer(serializers.Serializer):
    emprestimos = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False
    )

    def validate_emprestimos(self, value):
        emprestimos = list(map(lambda x: str(x), value))
        return list(set(emprestimos))

    def validate(self, data):
        try:
            data['emprestimos'] = DevolucaoService\
                .get_emprestimos_para_devolucao(data['emprestimos'])

        except APIException as e:
            raise serializers.ValidationError(str(e))

        return data

    def create(self, data):
        emprestimos = data['emprestimos']
        atendente_id = self.context['request'].user['_id']

        return DevolucaoService.save_devolucoes(emprestimos, atendente_id)

class RenovacaoEmprestimosSerializer(serializers.Serializer):
    emprestimos = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False
    )
    faz_emprestimo = serializers.BooleanField()

    def validate_emprestimos(self, value):
        return set(map(lambda x: str(x), value))

    def validate(self, data):
        emprestimos_id = data['emprestimos']
        usuario_id = None

        if not data['faz_emprestimo']:
            usuario_id = self.context['request'].user['_id']

        try:
            emprestimos, usuarios = EmprestimoService\
                .fetch_emprestimos_para_renovacao(emprestimos_id, usuario_id)

            data.update({
                'emprestimos': emprestimos,
                'usuarios': usuarios
            })

            return data

        except APIException as e:
            raise serializers.ValidationError(str(e))

    def create(self, data):
        emprestimos = data['emprestimos']
        usuarios = data['usuarios']
        agente_id = self.context['request'].user['_id']

        return EmprestimoService.save_renovacoes(emprestimos, usuarios, agente_id)
