# Generated by Django 3.0.8 on 2020-09-16 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circulacaoapp', '0003_emprestimo_livro_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emprestimo',
            name='atrasado',
        ),
    ]
