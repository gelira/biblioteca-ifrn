# Generated by Django 3.0.8 on 2020-09-12 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circulacaoapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emprestimo',
            name='exemplar_id',
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='exemplar_codigo',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
