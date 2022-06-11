from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import APIException

from ..utils import calcular_data_limite
from ..models import (
    Emprestimo, 
    Suspensao,
    Renovacao, 
    Reserva
)
from ..services import (
    AutenticacaoService,
    CatalogoService,
    EmprestimoService,
    ReservaService,
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
        agora = timezone.localtime()
        hoje = agora.date()
        data = agora.strftime('%d/%m/%Y')
        hora = agora.strftime('%H:%M:%S')
        
        suspensoes = {}
        codigos = []
        livros = []

        comprovantes = []
        atendente_id = self.context['request'].user['_id']

        with transaction.atomic():
            for emprestimo in emprestimos:
                diff = hoje - emprestimo.data_limite
                if diff.days > 0:
                    Suspensao.objects.create(
                        emprestimo=emprestimo,
                        usuario_id=emprestimo.usuario_id,
                        total_dias=diff.days
                    )

                    u_id = str(emprestimo.usuario_id)
                    if u_id not in suspensoes:
                        suspensoes[u_id] = 0
                    suspensoes[u_id] += diff.days

                codigos.append(emprestimo.exemplar_codigo)
                emprestimo.data_devolucao = hoje
                emprestimo.save()

                livro_id = str(emprestimo.livro_id)
                if livro_id not in livros:
                    livros.append(livro_id)

                comprovantes.append({
                    'usuario_id': str(emprestimo.usuario_id),
                    'atendente_id': atendente_id,
                    'livro_id': livro_id,
                    'atraso': diff.days,
                    'data': data,
                    'hora': hora,
                    'exemplar_codigo': emprestimo.exemplar_codigo,
                    'referencia': emprestimo.exemplar_referencia,
                })

            if suspensoes:
                AutenticacaoService.suspensoes(list(map(
                    lambda x: ({ 'usuario_id': x, 'dias': suspensoes[x] }), suspensoes)))

            CatalogoService.exemplares_devolvidos(codigos)
            
        DevolucaoService.call_enviar_comprovantes_devolucao(comprovantes)
        ReservaService.call_proximas_reservas(livros)

        return {}

class RenovacaoEmprestimosSerializer(serializers.Serializer):
    emprestimos = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False
    )
    faz_emprestimo = serializers.BooleanField()

    def validate_emprestimos(self, value):
        emprestimos = list(map(lambda x: str(x), value))
        return list(set(emprestimos))

    def validate(self, data):
        emprestimos_id = data['emprestimos']
        emprestimos = []
        usuarios = {}
        filtro = {}
        hoje = timezone.localdate()
        
        if not data['faz_emprestimo']:
            filtro['usuario_id'] = self.context['request'].user['_id']

        for e_id in emprestimos_id:
            filtro['_id'] = e_id
            
            emprestimo = Emprestimo.objects.filter(**filtro).first()
            if emprestimo is None:
                continue
            
            self.validar_emprestimo(emprestimo, hoje)
            usuario_id = str(emprestimo.usuario_id)
            if usuarios.get(usuario_id) is None:
                usuarios[usuario_id] = self.validar_usuario(usuario_id, hoje)
            
            emprestimos.append(emprestimo)

        data.update({
            'emprestimos': emprestimos,
            'usuarios': usuarios
        })
        return data

    def create(self, data):
        agente_id = self.context['request'].user['_id']
        emprestimos = data['emprestimos']
        usuarios = data['usuarios']

        agora = timezone.localtime()
        agora_data = agora.strftime('%d/%m/%Y')
        agora_hora = agora.strftime('%H:%M:%S')

        comprovantes = []

        with transaction.atomic():
            for emprestimo in emprestimos:
                usuario_id = str(emprestimo.usuario_id)

                perfil = usuarios[usuario_id]['perfil']
                emprestimo.quantidade_renovacoes += 1
                
                if emprestimo.quantidade_renovacoes >= perfil['quantidade_renovacoes']:
                    emprestimo.maximo_renovacoes = True
                
                nova_data = calcular_data_limite(perfil['max_dias'])
                emprestimo.data_limite = nova_data
                
                Renovacao.objects.create(
                    emprestimo=emprestimo,
                    nova_data_limite=nova_data,
                    usuario_id=agente_id
                )
                emprestimo.save()

                comprovantes.append({
                    'usuario_id': usuario_id,
                    'livro_id': str(emprestimo.livro_id),
                    'data_limite': nova_data.strftime('%d/%m/%Y'),
                    'data': agora_data,
                    'hora': agora_hora,
                    'exemplar_codigo': emprestimo.exemplar_codigo,
                    'atendente_id': agente_id if agente_id != usuario_id else '' 
                })

        EmprestimoService.call_enviar_comprovantes_renovacao(comprovantes)

        return {}

    def validar_emprestimo(self, emprestimo, hoje):
        if emprestimo.data_devolucao is not None:
            raise serializers.ValidationError('Não é possível renovar empréstimo devolvido')

        if emprestimo.data_limite < hoje:
            raise serializers.ValidationError('Há empréstimos atrasados')

        if emprestimo.maximo_renovacoes:
            raise serializers.ValidationError('Há empréstimos com máximo de renovações')

        if emprestimo.exemplar_referencia:
            raise serializers.ValidationError('Não é possível renovar empréstimo de exemplar referência')

        if Reserva.objects.filter(
            livro_id=emprestimo.livro_id,
            emprestimo_id=None,
            cancelada=False,
            disponibilidade_retirada=None,
        ).exists():
            raise serializers.ValidationError('Existem reservas para esse exemplar, não é possível renovar o empréstimo')
        
    def validar_usuario(self, usuario_id, hoje):
        usuario = self.buscar_usuario(usuario_id)

        suspensao = usuario['suspensao']
        if suspensao is not None:
            suspensao = timezone.datetime.strptime(suspensao, '%Y-%m-%d').date() 
            if suspensao >= hoje:
                raise serializers.ValidationError('Usuário suspenso')

        if Emprestimo.objects.filter(
            usuario_id=usuario_id,
            data_devolucao=None,
            data_limite__lt=hoje
        ).exists():
            raise serializers.ValidationError('Usuário com empréstimos atrasados')

        return usuario

    def buscar_usuario(self, usuario_id):
        try:
            return AutenticacaoService.consulta_usuario(usuario_id)

        except APIException:
            raise serializers.ValidationError('Não foi possível obter informações do usuário')
