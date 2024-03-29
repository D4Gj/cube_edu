# Generated by Django 3.2.12 on 2022-04-26 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_content_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='visible',
            field=models.BooleanField(default=False, verbose_name='Видимость контента'),
        ),
        migrations.AlterField(
            model_name='content',
            name='visible',
            field=models.BooleanField(default=False, verbose_name='Видимость контента'),
        ),
    ]
