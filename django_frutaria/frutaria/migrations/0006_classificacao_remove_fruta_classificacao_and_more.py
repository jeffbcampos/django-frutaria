# Generated by Django 5.0.4 on 2024-07-06 16:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frutaria', '0005_alter_fruta_preco_alter_vendas_valor_venda'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='fruta',
            name='classificacao',
        ),
        migrations.RemoveField(
            model_name='fruta',
            name='qtd_estoque',
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtd_estoque', models.IntegerField()),
                ('classificacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frutaria.classificacao')),
                ('fruta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frutaria.fruta')),
            ],
        ),
        migrations.AddField(
            model_name='fruta',
            name='classificacoes',
            field=models.ManyToManyField(through='frutaria.Estoque', to='frutaria.classificacao'),
        ),
    ]
