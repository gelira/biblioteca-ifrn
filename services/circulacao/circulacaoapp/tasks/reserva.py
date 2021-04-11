from __future__ import absolute_import, unicode_literals

import os
from django.db import transaction
from django.utils import timezone
from circulacaoapp.models import Reserva, Data
from circulacaoapp.utils import calcular_data_limite
from circulacaoapp import calls
from circulacao.celery import app

PROJECT_NAME = os.getenv('PROJECT_NAME')

def _verificar_reservas():
    data = timezone.localdate() - timezone.timedelta(days=1)
    
    if data.weekday() > 4: 
        # Sábado ou Domingo
        return

    if Data.objects.filter(
        dia=data.day, 
        mes=data.month, 
        ano=data.year
    ).exists():
        return

    comprovantes = []
    disponibilidade_retirada = None
    data_limite = None
    agora = timezone.localtime()

    reservas = Reserva.objects.filter(
        disponibilidade_retirada__lt=data,
        emprestimo_id=None,
        cancelada=False
    ).all()

    data = agora.strftime('%d/%m/%Y')
    hora = agora.strftime('%H:%M:%S')

    with transaction.atomic():
        for reserva in reservas:
            reserva.cancelada = True
            reserva.save()

            proxima_reserva = Reserva.objects.filter(
                disponibilidade_retirada=None,
                livro_id=reserva.livro_id,
                emprestimo_id=None,
                cancelada=False
            ).first()

            if proxima_reserva is not None:
                if disponibilidade_retirada is None:
                    disponibilidade_retirada = calcular_data_limite(1)
                    data_limite = disponibilidade_retirada.strftime('%d/%m/%Y')

                proxima_reserva.disponibilidade_retirada = calcular_data_limite(1)
                proxima_reserva.save()

                comprovantes.append({
                    'usuario_id': str(proxima_reserva.usuario_id),
                    'livro_id': str(proxima_reserva.livro_id),
                    'data': data,
                    'hora': hora,
                    'data_limite': data_limite
                })

    app.send_task(
        'circulacaoapp.tasks.enviar_reservas_disponiveis',
        [comprovantes],
        queue=PROJECT_NAME
    )

def _enviar_reservas_disponiveis(comprovantes):
    usuarios = {}
    livros = {}

    for comprovante in comprovantes:
        usuario_id = comprovante['usuario_id']
        livro_id = comprovante['livro_id']

        if usuario_id not in usuarios:
            r = calls.autenticacao.api_consulta_usuario(usuario_id)
            r.raise_for_status()
            usuarios[usuario_id] = r.json()

        if livro_id not in livros:
            r = calls.catalogo.api_get_livro(livro_id, { 'min': '1' })
            r.raise_for_status()
            livros[livro_id] = r.json()

        usuario = usuarios[usuario_id]
        livro = livros[livro_id]

        emails = [usuario['email_institucional']]
        if usuario['email_pessoal']:
            emails.append(usuario['email_pessoal'])

        comprovante.update({
            'nome_usuario': usuario['nome'],
            'titulo_livro': livro['titulo']
        })

        calls.notificacao.task_reserva_disponivel(comprovante, emails)
