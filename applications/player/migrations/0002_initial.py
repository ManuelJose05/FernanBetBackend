# Generated by Django 5.2 on 2025-05-03 14:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('player', '0001_initial'),
        ('school', '0001_initial'),
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='equipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.team'),
        ),
        migrations.AddField(
            model_name='player',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school'),
        ),
    ]
