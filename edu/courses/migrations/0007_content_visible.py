# Generated by Django 3.2.12 on 2022-04-26 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20220419_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='visible',
            field=models.BooleanField(default=False, verbose_name='Видимость модуля'),
        ),
    ]