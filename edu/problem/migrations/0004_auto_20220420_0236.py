# Generated by Django 3.2.12 on 2022-04-19 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0003_auto_20220420_0223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='input_description',
            new_name='description_input',
        ),
        migrations.RenameField(
            model_name='problem',
            old_name='output_description',
            new_name='description_output',
        ),
    ]