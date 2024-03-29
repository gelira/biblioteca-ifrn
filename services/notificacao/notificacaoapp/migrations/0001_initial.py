# Generated by Django 3.0.8 on 2021-09-08 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('usuario_id', models.UUIDField()),
                ('nome', models.CharField(max_length=150)),
                ('matricula', models.CharField(max_length=150)),
                ('email_institucional', models.EmailField(max_length=254)),
                ('email_pessoal', models.EmailField(blank=True, max_length=254)),
            ],
            options={
                'db_table': 'contatos',
            },
        ),
    ]
