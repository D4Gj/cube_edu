# Generated by Django 3.2.12 on 2022-04-19 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='result',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
