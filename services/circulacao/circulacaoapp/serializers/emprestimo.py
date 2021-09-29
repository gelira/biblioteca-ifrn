from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from ..utils import calcular_data_limite
from ..models import (
    Emprestimo, 
    Suspensao,
    Renovacao, 
    Reserva,
    Data
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

        usuario = self.validar_usuario(matricula, senha)
        self.validar_usuario_suspenso(usuario)

        livros_emprestados = self.validar_emprestimos_usuario(
            usuario['_id'], 
            usuario['perfil']['max_livros'], 
            len(codigos)
        )
        exemplares, reservas = self.validar_codigos(codigos, livros_emprestados, usuario['_id'])

        data['usuario'] = usuario
        data['exemplares'] = exemplares
        data['reservas'] = reservas
        return data

    def create(self, data):
        data_limite = None
        data_limite_referencia = None
        
        usuario = data['usuario']
        reservas = data['reservas']
        emprestimos = []

        exemplares_email = []
        alertas = []

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

                reserva = reservas.get(livro_id)
                if reserva is not None:
                    reserva.emprestimo = e
                    reserva.save()

                emprestimos.append(e)

                titulo = exemplar['livro']['titulo']
                codigo = exemplar['codigo']
                dl = e.data_limite.strftime('%d/%m/%Y')

                exemplares_email.append({
                    'titulo': titulo,
                    'codigo': codigo,
                    'referencia': exemplar['referencia'],
                    'data_limite': dl
                })

                alertas.append({
                    'usuario_id': usuario['_id'],
                    'emprestimo_id': str(e._id),
                    'titulo': titulo,
                    'exemplar_codigo': codigo,
                    'data_limite': dl,
                })

        self.enviar_comprovante(usuario['_id'], exemplares_email)
        CatalogoService.exemplares_emprestados(data['codigos'])
        EmprestimoService.call_agendar_alertas_emprestimo(alertas)

        return emprestimos

    def validate_codigos(self, value):
        return list(set(value))

    def validar_usuario(self, matricula, senha):
        try:
            return AutenticacaoService.autenticar_usuario(matricula, senha)

        except Exception as e:
            arg = e.args[0]
            
            if isinstance(arg, dict):
                raise serializers.ValidationError(arg.get('error'))
            
            raise e

    def validar_codigos(self, codigos, livros_emprestados, usuario_id):
        try:
            hoje = timezone.localdate()

            emprestar_referencia = None
            exemplares = []
            reservas = {}

            for codigo in codigos:
                exemplar = CatalogoService.consulta_codigo_exemplar(codigo)
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

                reserva = Reserva.objects.filter(
                    Q(disponibilidade_retirada=None) | Q(disponibilidade_retirada__gte=hoje),
                    usuario_id=usuario_id,
                    livro_id=livro_id,
                    cancelada=False,
                    emprestimo_id=None
                ).first()

                if reserva is not None:
                    reservas[livro_id] = reserva
                else:
                    exemplares_disponiveis = exemplar['livro']['exemplares_disponiveis']
                    qtd_reservas = Reserva.objects.filter(
                        Q(disponibilidade_retirada=None) | Q(disponibilidade_retirada__gte=hoje),
                        livro_id=livro_id,
                        cancelada=False,
                        emprestimo_id=None
                    ).count()
                    if exemplares_disponiveis <= qtd_reservas:
                        raise serializers.ValidationError('Existem reservas para o exemplar {}'.format(codigo))
                
                livros_emprestados.append(livro_id)
                exemplares.append(exemplar)

            return exemplares, reservas

        except serializers.ValidationError as e:
            raise e

        except:
            raise serializers.ValidationError('Erro de comunicação entre os serviços')

    def validar_usuario_suspenso(self, usuario):
        suspensao = usuario['suspensao']
        hoje = timezone.localdate()

        if suspensao is not None:
            suspensao = timezone.datetime.strptime(suspensao, '%Y-%m-%d').date()
            if suspensao >= hoje:
                raise serializers.ValidationError('Usuário suspenso')

        if Emprestimo.objects.filter(
            usuario_id=usuario['_id'],
            data_devolucao=None,
            data_limite__lt=hoje
        ).exists():
            raise serializers.ValidationError('Usuário com empréstimos atrasados')

    def validar_emprestimos_usuario(self, usuario_id, max_livros, quantidade_livros):
        emprestimos_vigentes = list(Emprestimo.objects.filter(
            usuario_id=usuario_id,
            data_devolucao=None
        ).values_list('livro_id', flat=True).all())

        if (len(emprestimos_vigentes) + quantidade_livros) > max_livros:
            raise serializers.ValidationError('Atingido o limite de livros para o usuário')

        return list(map(lambda x: str(x), emprestimos_vigentes))

    def emprestar_exemplar_referencia(self):
        hoje = timezone.localdate()

        if hoje.weekday() == 4:
            return True

        amanha = hoje + timezone.timedelta(days=1)
        return Data.objects.filter(dia=amanha.day, mes=amanha.month, ano=amanha.year).exists()

    def enviar_comprovante(self, usuario_id, exemplares):
        atendente_id = self.context['request'].user['_id']
        agora = timezone.localtime()

        contexto = {
            'usuario_id': usuario_id,
            'atendente_id': atendente_id,
            'data': agora.strftime('%d/%m/%Y'),
            'hora': agora.strftime('%H:%M:%S'),
            'exemplares': exemplares
        }

        EmprestimoService.call_enviar_comprovante_emprestimo(contexto)

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
            emprestimo = Emprestimo.objects.filter(
                _id=e_id,
                data_devolucao=None
            ).first()

            if emprestimo is not None:
                emprestimos.append(emprestimo)

        if len(emprestimos) == 0:
            raise serializers.ValidationError('Nenhum empréstimo foi encontrado')

        data['emprestimos'] = emprestimos
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
            AutenticacaoService.suspensoes(suspensoes)

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
            return AutenticacaoService.informacoes_usuario(usuario_id)

        except Exception as e:
            arg = e.args[0]
            
            if isinstance(arg, dict):
                raise serializers.ValidationError(arg.get('error'))
            
            raise e
