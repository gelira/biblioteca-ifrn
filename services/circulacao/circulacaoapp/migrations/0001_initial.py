# Generated by Django 3.0.8 on 2020-08-31 04:00

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Abono',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('usuario_id', models.UUIDField()),
                ('justificativa', models.TextField()),
            ],
            options={
                'db_table': 'abonos',
            },
        ),
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('usuario_id', models.UUIDField()),
                ('exemplar_id', models.UUIDField()),
                ('data_emprestimo', models.DateField(auto_now_add=True)),
                ('data_limite', models.DateField()),
                ('data_devolucao', models.DateField(null=True)),
                ('quantidade_renovacoes', models.PositiveIntegerField(default=0)),
                ('atrasado', models.BooleanField(default=False)),
                ('avaliado', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'emprestimos',
                'ordering': ['data_emprestimo'],
            },
        ),
        migrations.CreateModel(
            name='Feriado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'feriados',
            },
        ),
        migrations.CreateModel(
            name='Suspensao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_id', models.UUIDField()),
                ('total_dias', models.PositiveIntegerField()),
                ('dias_restantes', models.PositiveIntegerField()),
                ('abono', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='suspensoes', to='circulacaoapp.Abono')),
                ('emprestimo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='suspensoes', to='circulacaoapp.Emprestimo')),
            ],
            options={
                'db_table': 'suspensoes',
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('usuario_id', models.UUIDField()),
                ('livro_id', models.UUIDField()),
                ('momento', models.DateTimeField(auto_now_add=True)),
                ('disponivel', models.DateTimeField(null=True)),
                ('cancelada', models.BooleanField(default=False)),
                ('emprestimo', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='circulacaoapp.Emprestimo')),
            ],
            options={
                'db_table': 'reservas',
                'ordering': ['-momento'],
            },
        ),
        migrations.CreateModel(
            name='Renovacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_renovacao', models.DateField(auto_now_add=True)),
                ('nova_data_limite', models.DateField()),
                ('agente', models.CharField(max_length=100)),
                ('emprestimo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='renovacoes', to='circulacaoapp.Emprestimo')),
            ],
            options={
                'db_table': 'renovacoes',
                'ordering': ['data_renovacao'],
            },
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.PositiveIntegerField()),
                ('mes', models.PositiveIntegerField()),
                ('ano', models.PositiveIntegerField()),
                ('feriado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datas', to='circulacaoapp.Feriado')),
            ],
            options={
                'db_table': 'datas',
            },
        ),
    ]
