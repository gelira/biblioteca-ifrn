# Generated by Django 3.0.8 on 2020-11-03 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circulacaoapp', '0010_suspensao__id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reserva',
            options={'ordering': ['-created']},
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='momento',
        ),
    ]
