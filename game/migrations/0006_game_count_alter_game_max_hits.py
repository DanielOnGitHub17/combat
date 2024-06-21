# Generated by Django 5.0.6 on 2024-06-20 18:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_remove_game_n_bots_remove_game_n_real'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='count',
            field=models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='game',
            name='max_hits',
            field=models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(7)]),
        ),
    ]
