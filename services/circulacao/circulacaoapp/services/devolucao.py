from operator import imod
import os
from celery import group

from circulacao.celery import app

from .autenticacao import AutenticacaoService
from .catalogo import CatalogoService
from .notificacao import NotificacaoService

CIRCULACAO_QUEUE = os.getenv('PROJECT_NAME')

class DevolucaoService:
    @classmethod
    def enviar_comprovante_devolucao(cls, contexto):
        usuario_id = contexto['usuario_id']
        livro_id = contexto['livro_id']

        usuario = AutenticacaoService.informacoes_usuario(usuario_id)
        livro = CatalogoService.busca_livro(livro_id, min=True)

        emails = [usuario['email_institucional']]
        if usuario['email_pessoal']:
            emails.append(usuario['email_pessoal'])

        contexto.update({
            'nome_usuario': usuario['nome'],
            'titulo': livro['titulo']
        })

        NotificacaoService.comprovante_devolucao(contexto, emails)

    @classmethod
    def call_enviar_comprovantes_devolucao(cls, comprovantes):
        group([
            app.signature(
                'circulacao.enviar_comprovante_devolucao',
                args=[comprovante],
                queue=CIRCULACAO_QUEUE,
                ignore_result=True
            ) for comprovante in comprovantes
        ])()
