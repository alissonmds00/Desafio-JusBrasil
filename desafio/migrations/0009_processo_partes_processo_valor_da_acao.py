# Generated by Django 5.1 on 2024-08-21 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desafio', '0008_remove_processo_valor_da_acao'),
    ]

    operations = [
        migrations.AddField(
            model_name='processo',
            name='partes',
            field=models.TextField(default='Nenhum envolvido encontrado'),
        ),
        migrations.AddField(
            model_name='processo',
            name='valor_da_acao',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
