# Generated by Django 5.1.6 on 2025-02-15 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pacientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('telefone', models.CharField(blank=True, max_length=255, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos')),
                ('pagamento_em_dia', models.BooleanField(default=True)),
                ('data_pagamento', models.DateField(blank=True, null=True)),
                ('queixa_principal', models.TextField(choices=[('TDHA', 'TDHA'), ('D', 'Depressao'), ('A', 'Ansiedade'), ('TAG', 'Transtorno de ansiedade generalizada')], max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
