# Generated by Django 5.0.1 on 2024-03-02 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_remove_player_id_alter_game_creator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.CharField(max_length=30),
        ),
    ]
