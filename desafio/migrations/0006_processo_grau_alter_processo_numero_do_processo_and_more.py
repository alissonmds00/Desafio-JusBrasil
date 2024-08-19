# Generated by Django 5.1 on 2024-08-19 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desafio', '0005_rename_numero_processo_numero_do_processo'),
    ]

    operations = [
        migrations.AddField(
            model_name='processo',
            name='grau',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='processo',
            name='numero_do_processo',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='processo',
            unique_together={('numero_do_processo', 'grau')},
        ),
    ]
