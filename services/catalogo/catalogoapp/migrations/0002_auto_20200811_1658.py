# Generated by Django 3.0.8 on 2020-08-11 16:58

import catalogoapp.models.livro
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogoapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livro',
            name='foto_capa',
            field=models.ImageField(blank=True, upload_to=catalogoapp.models.livro.nome_arquivo),
        ),
    ]