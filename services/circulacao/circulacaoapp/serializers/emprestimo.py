import os
import requests
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from ..models import (
    Emprestimo, 
    Suspensao,
    Renovacao, 
    Reserva,
    Data
)
from ..tasks import (
    marcar_exemplares_emprestados,
    marcar_exemplares_devolvidos,
    usuarios_suspensos
)

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')
CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')

def calcular_data_limite(max_dias=None):
    hoje = timezone.now().date()

    if max_dias is not None:
        hoje = hoje + timezone.timedelta(days=max_dias)
    
    while True:
        if hoje.weekday() < 5:
            if not Data.objects.filter(dia=hoje.day, mes=hoje.month, ano=hoje.year).exists():
                return hoje
        hoje = hoje + timezone.timedelta(days=1)

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

        usuario = self.validar_usuario(matricula, senha)
        self.validar_usuario_suspenso(usuario)

        livros_emprestados = self.validar_emprestimos_usuario(
            usuario['_id'], 
            usuario['perfil']['max_livros'], 
            len(codigos)
        )
        exemplares = self.validar_codigos(codigos, livros_emprestados)

        data['usuario'] = usuario
        data['exemplares'] = exemplares
        return data

    def create(self, data):
        agora = timezone.now()
        
        data_limite = None
        data_limite_referencia = None
        
        usuario = data['usuario']
        emprestimos = []

        with transaction.atomic():
            for exemplar in data['exemplares']:
                livro_id = exemplar['livro']['_id']
                e = Emprestimo(
                    usuario_id=usuario['_id'],
                    livro_id=livro_id,
                    exemplar_codigo=exemplar['codigo'],
                    exemplar_referencia=exemplar['referencia']
                )
                if data_limite is None:
                    if not exemplar['referencia']:
                        data_limite = calcular_data_limite(usuario['perfil']['max_dias'])
                
                if data_limite_referencia is None:
                    if exemplar['referencia']:
                        data_limite_referencia = calcular_data_limite()

                e.data_limite = data_limite_referencia if exemplar['referencia'] else data_limite
                e.save()

                reserva = Reserva.objects.filter(
                    Q(disponibilidade_retirada=None) | Q(disponibilidade_retirada__gt=agora),
                    usuario_id=usuario['_id'],
                    livro_id=livro_id,
                    cancelada=False,
                    emprestimo_id=None
                ).first()
                if reserva is not None:
                    reserva.emprestimo = e
                    reserva.save()

                emprestimos.append(e)

        marcar_exemplares_emprestados.delay(self.context['request'].user['_id'], data['codigos'])
        return emprestimos

    def validate_codigos(self, value):
        return list(set(value))

    def validar_usuario(self, matricula, senha):
        try:
            r1 = requests.post(AUTENTICACAO_SERVICE_URL + '/token', json={
                'username': matricula, 
                'password': senha
            })

            if not r1.ok:
                if r1.status_code == 401:
                    raise serializers.ValidationError('Usuário ou senha inválidos')
                raise serializers.ValidationError('Erro ao autenticar usuário')

            token = r1.json()['token']
            r2 = requests.get(AUTENTICACAO_SERVICE_URL + '/informacoes', headers={
                'Authorization': 'JWT {}'.format(token)
            })
            
            if not r2.ok:
                raise serializers.ValidationError('Erro ao buscar informações do usuário')
            return r2.json()

        except serializers.ValidationError as e:
            raise e

        except:
            raise serializers.ValidationError('Erro de comunicação entre os serviços')

    def validar_codigos(self, codigos, livros_emprestados):
        try:
            emprestar_referencia = None
            exemplares = []
            for codigo in codigos:
                r = requests.get(CATALOGO_SERVICE_URL + '/exemplares/consulta/' + codigo)
                if not r.ok:
                    raise serializers.ValidationError('Exemplar {} não encontrado'.format(codigo))
                
                exemplar = r.json()
                if not exemplar['ativo']:
                    raise serializers.ValidationError('Exemplar {} inativo'.format(codigo))

                if not exemplar['disponivel']:
                    raise serializers.ValidationError('Exemplar {} indisponível'.format(codigo))

                if exemplar['referencia']:
                    if emprestar_referencia is None:
                        emprestar_referencia = self.emprestar_exemplar_referencia()

                    if not emprestar_referencia:
                        raise serializers.ValidationError('Exemplar {} referência, não pode ser emprestado hoje'.format(codigo))

                livro_id = exemplar['livro']['_id']
                if livro_id in livros_emprestados:
                    raise serializers.ValidationError('Usuário não pode pegar dois exemplares do mesmo livro')
                
                livros_emprestados.append(livro_id)
                exemplares.append(exemplar)

            return exemplares

        except serializers.ValidationError as e:
            raise e

        except:
            raise serializers.ValidationError('Erro de comunicação entre os serviços')

    def validar_usuario_suspenso(self, usuario):
        suspensao = usuario['suspensao']
        hoje = timezone.now().date()

        if suspensao is not None:
            suspensao = timezone.datetime.strptime(suspensao, '%Y-%m-%d').date()
            if suspensao >= hoje:
                raise serializers.ValidationError('Usuário suspenso')

        if Emprestimo.objects.filter(**{
            'usuario_id': usuario['_id'],
            'data_devolucao': None,
            'data_limite__lt': hoje
        }).exists():
            raise serializers.ValidationError('Usuário com empréstimos atrasados')

    def validar_emprestimos_usuario(self, usuario_id, max_livros, quantidade_livros):
        emprestimos_vigentes = list(Emprestimo.objects.filter(**{
            'usuario_id': usuario_id,
            'data_devolucao': None
        }).values_list('livro_id', flat=True).all())

        if (len(emprestimos_vigentes) + quantidade_livros) > max_livros:
            raise serializers.ValidationError('Atingido o limite de livros para o usuário')

        return list(map(lambda x: str(x), emprestimos_vigentes))

    def emprestar_exemplar_referencia(self):
        hoje = timezone.now().date()

        if hoje.weekday() == 4:
            return True

        while hoje.weekday() < 5:
            if not Data.objects.filter(dia=hoje.day, mes=hoje.month, ano=hoje.year).exists():
                return False
            hoje = hoje + timezone.timedelta(days=1)
        
        return True

class DevolucaoEmprestimosSerializer(serializers.Serializer):
    emprestimos = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False
    )

    def validate_emprestimos(self, value):
        emprestimos = list(map(lambda x: str(x), value))
        return list(set(emprestimos))

    def validate(self, data):
        emprestimos = []
        emprestimos_id = data['emprestimos']
        
        for e_id in emprestimos_id:
            emprestimo = Emprestimo.objects.filter(**{
                '_id': e_id,
                'data_devolucao': None
            }).first()

            if emprestimo is not None:
                emprestimos.append(emprestimo)

        if len(emprestimos) == 0:
            raise serializers.ValidationError('Nenhum empréstimo foi encontrado')

        data['emprestimos'] = emprestimos
        return data

    def create(self, data):
        emprestimos = data['emprestimos']
        hoje = timezone.now().date()
        
        suspensoes = {}
        codigos = []

        with transaction.atomic():
            for emprestimo in emprestimos:
                diff = hoje - emprestimo.data_limite
                if diff.days > 0:
                    Suspensao.objects.create(**{
                        'emprestimo': emprestimo,
                        'usuario_id': emprestimo.usuario_id,
                        'total_dias': diff.days
                    })

                    u_id = str(emprestimo.usuario_id)
                    if u_id not in suspensoes:
                        suspensoes[u_id] = 0
                    suspensoes[u_id] += diff.days

                codigos.append(emprestimo.exemplar_codigo)
                emprestimo.data_devolucao = hoje
                emprestimo.save()

                reserva = Reserva.objects.filter(
                    disponibilidade_retirada=None,
                    livro_id=emprestimo.livro_id,
                    cancelada=False,
                    emprestimo_id=None
                ).first()
                if reserva is not None:
                    reserva.disponibilidade_retirada = calcular_data_limite(1)
                    reserva.save()

        usuario_id = self.context['request'].user['_id']
        if suspensoes:
            usuarios_suspensos.delay(usuario_id, suspensoes)
        marcar_exemplares_devolvidos.delay(usuario_id, codigos)

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
        hoje = timezone.now().date()
        
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

        with transaction.atomic():
            for emprestimo in emprestimos:
                perfil = usuarios[str(emprestimo.usuario_id)]['perfil']
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
        
    def validar_usuario(self, usuario_id, hoje):
        usuario = self.buscar_usuario(usuario_id)

        suspensao = usuario['suspensao']
        if suspensao is not None:
            suspensao = timezone.datetime.strptime(suspensao, '%Y-%m-%d').date() 
            if suspensao >= hoje:
                raise serializers.ValidationError('Usuário suspenso')

        if Emprestimo.objects.filter(**{
            'usuario_id': usuario_id,
            'data_devolucao': None,
            'data_limite__lt': hoje
        }).exists():
            raise serializers.ValidationError('Usuário com empréstimos atrasados')

        return usuario

    def buscar_usuario(self, usuario_id):
        r = requests.get(AUTENTICACAO_SERVICE_URL + '/consulta', params={'id': usuario_id}, headers={
            'X-Usuario-Id': self.context['request'].user['_id']
        })
        if not r.ok:
            raise serializers.ValidationError('Erro ao buscar informações do usuário')

        return r.json()
