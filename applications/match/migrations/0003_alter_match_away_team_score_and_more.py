# Generated by Django 5.2 on 2025-05-29 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0002_match_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='away_team_score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='local_team_score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
