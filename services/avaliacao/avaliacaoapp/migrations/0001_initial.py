# Generated by Django 3.0.8 on 2020-11-18 10:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('tag', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'tags',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('usuario_id', models.UUIDField()),
                ('emprestimo_id', models.UUIDField()),
                ('livro_id', models.UUIDField()),
                ('nota', models.PositiveIntegerField()),
                ('comentario', models.TextField(blank=True)),
                ('tags', models.ManyToManyField(db_table='avaliacoes_tags', to='avaliacaoapp.Tag')),
            ],
            options={
                'db_table': 'avaliacoes',
                'ordering': ['-created'],
            },
        ),
    ]
