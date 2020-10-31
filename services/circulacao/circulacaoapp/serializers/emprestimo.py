import os
import requests
from datetime import date, timedelta
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from ..models import (
    Emprestimo, 
    Suspensao, 
    Data
)
from ..tasks import marcar_exemplares_emprestados

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')
CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')

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
        self.validar_usuario_suspenso(usuario['_id'])

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
        data_limite = None
        data_limite_referencia = None
        usuario = data['usuario']
        emprestimos = []

        with transaction.atomic():
            for exemplar in data['exemplares']:
                e = Emprestimo(
                    usuario_id=usuario['_id'],
                    livro_id=exemplar['livro']['_id'],
                    exemplar_codigo=exemplar['codigo']
                )
                if data_limite is None:
                    if not exemplar['referencia']:
                        data_limite = self.calcular_data_limite(usuario['perfil']['max_dias'])
                
                if data_limite_referencia is None:
                    if exemplar['referencia']:
                        data_limite_referencia = self.calcular_data_limite()

                e.data_limite = data_limite_referencia if exemplar['referencia'] else data_limite
                e.save()

                emprestimos.append(e)

        marcar_exemplares_emprestados.delay(self.context['request'].user['_id'], data['codigos'])
        return emprestimos

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

    def validar_usuario_suspenso(self, usuario_id):
        suspenso = Suspensao.objects.filter(**{
            'usuario_id': usuario_id,
            'abono': None,
            'dias_restantes__gt': 0
        }).exists()

        emprestimo_atrasado = Emprestimo.objects.filter(**{
            'usuario_id': usuario_id,
            'data_devolucao': None,
            'data_limite__lt': date.today()
        }).exists()

        if suspenso or emprestimo_atrasado:
            raise serializers.ValidationError('Usuário suspenso')

    def validar_emprestimos_usuario(self, usuario_id, max_livros, quantidade_livros):
        emprestimos_vigentes = list(Emprestimo.objects.filter(**{
            'usuario_id': usuario_id,
            'data_devolucao': None
        }).values_list('livro_id', flat=True).all())

        if (len(emprestimos_vigentes) + quantidade_livros) > max_livros:
            raise serializers.ValidationError('Atingido o limite de livros para o usuário')

        return list(map(lambda x: str(x), emprestimos_vigentes))

    def emprestar_exemplar_referencia(self):
        hoje = date.today()

        if hoje.weekday() == 4:
            return True

        while hoje.weekday() < 5:
            if not Data.objects.filter(dia=hoje.day, mes=hoje.month, ano=hoje.year).exists():
                return False
            hoje = hoje + timedelta(days=1)
        
        return True

    def calcular_data_limite(self, max_dias=None):
        hoje = date.today()

        if max_dias is not None:
            hoje = hoje + timedelta(days=max_dias)
        
        while True:
            if hoje.weekday() < 5:
                if not Data.objects.filter(dia=hoje.day, mes=hoje.month, ano=hoje.year).exists():
                    return hoje
            hoje = hoje + timedelta(days=1)

class DevolucaoEmprestimosSerializer(serializers.Serializer):
    codigos = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )

    def validate_codigos(self, value):
        return list(set(value))

    def validate(self, data):
        emprestimos = []
        codigos = data['codigos']
        
        for codigo in codigos:
            emprestimo = Emprestimo.objects.filter(**{
                'exemplar_codigo': codigo,
                'data_devolucao': None
            }).order_by('-created').first()

            if emprestimo is not None:
                emprestimos.append(emprestimo)

        if len(emprestimos) == 0:
            raise serializers.ValidationError('Nenhum empréstimo foi encontrado')

        data['emprestimos'] = emprestimos
        return data

    def create(self, data):
        emprestimos = data['emprestimos']
        for emprestimo in emprestimos:
            hoje = timezone.now().date()
            if hoje > emprestimo.data_limite:
                diff = hoje - emprestimo.data_limite
                Suspensao.objects.create(**{
                    'emprestimo': emprestimo,
                    'usuario_id': emprestimo.usuario_id,
                    'total_dias': diff.days
                })

            emprestimo.data_devolucao = hoje
            emprestimo.save()

        return {}
