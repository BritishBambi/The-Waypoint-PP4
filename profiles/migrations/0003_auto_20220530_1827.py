# Generated by Django 3.2.13 on 2022-05-30 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_rename_game_id_game_gameid'),
        ('profiles', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='played',
            field=models.ManyToManyField(blank=True, related_name='played', to='game.Game'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='to_play',
            field=models.ManyToManyField(blank=True, related_name='to_play', to='game.Game'),
        ),
    ]
