# Generated by Django 3.2.13 on 2022-08-06 13:23

from django.db import migrations

PERMISSOES = [
    ('perfil.gerenciar', 'Gerenciar perfis'),
]

def create_permissoes(apps, schema_editor):
    Permissao = apps.get_model('autenticacaoapp', 'Permissao')
    for perm in PERMISSOES:
        Permissao.objects.create(codigo=perm[0], descricao=perm[1])

class Migration(migrations.Migration):

    dependencies = [
        ('autenticacaoapp', '0015_auto_20220525_1946'),
    ]

    operations = [
        migrations.RunPython(create_permissoes),
    ]
