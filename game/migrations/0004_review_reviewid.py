# Generated by Django 3.2.13 on 2022-05-31 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='reviewID',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]