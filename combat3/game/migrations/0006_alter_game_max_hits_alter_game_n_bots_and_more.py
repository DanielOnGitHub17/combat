# Generated by Django 5.0.1 on 2024-03-02 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_game_data_game_initial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='max_hits',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='game',
            name='n_bots',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='game',
            name='n_real',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='game',
            name='size',
            field=models.IntegerField(default=15),
        ),
    ]
