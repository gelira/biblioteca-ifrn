# Generated by Django 3.0.8 on 2020-08-30 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogoapp', '0003_exemplar_ativo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='localizacaofisica',
            old_name='disponivel',
            new_name='ativo',
        ),
    ]
