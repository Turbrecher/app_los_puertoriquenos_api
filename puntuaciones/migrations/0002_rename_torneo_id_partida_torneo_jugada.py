# Generated by Django 5.0.7 on 2024-07-10 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puntuaciones', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partida',
            old_name='torneo_id',
            new_name='torneo',
        ),
        migrations.CreateModel(
            name='Jugada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntacion', models.IntegerField()),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puntuaciones.jugador')),
                ('partida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puntuaciones.partida')),
            ],
        ),
    ]
