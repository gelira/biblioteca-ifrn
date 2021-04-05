from __future__ import absolute_import, unicode_literals

from circulacaoapp import calls

def _enviar_comprovantes_devolucao(comprovantes):
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
            'titulo': livro['titulo']
        })

        calls.notificacao.task_comprovante_devolucao(comprovante, emails)
