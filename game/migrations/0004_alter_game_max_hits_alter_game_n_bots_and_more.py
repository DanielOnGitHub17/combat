# Generated by Django 5.0.6 on 2024-06-20 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_alter_player_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='max_hits',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='game',
            name='n_bots',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='game',
            name='n_real',
            field=models.IntegerField(),
        ),
    ]
