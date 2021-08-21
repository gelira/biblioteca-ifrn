# Generated by Django 3.0.8 on 2020-09-03 01:07

from django.db import migrations

PERMISSOES = [
    ('emprestimo.fazer', 'Fazer emprestimo'),
    ('emprestimo.receber_devolucao', 'Receber devolução de empréstimo'),
    ('suspensao.abonar', 'Abonar suspensão'),
    ('livro.catalogar', 'Catalogar livro'),
    ('livro.modificar', 'Modificar livro'),
    ('avaliacao.moderar', 'Moderar avaliação'),
    ('avaliacao.selecionar', 'Selecionar avaliações'),
    ('bolsista.promover', 'Promover bolsista')
]

def create_permissoes_padrao(apps, schema_editor):
    Permissao = apps.get_model('autenticacaoapp', 'Permissao')
    for perm in PERMISSOES:
        Permissao.objects.create(codigo=perm[0], descricao=perm[1])

class Migration(migrations.Migration):

    dependencies = [
        ('autenticacaoapp', '0005_permissao_permissaousuario'),
    ]

    operations = [
        migrations.RunPython(create_permissoes_padrao)
    ]