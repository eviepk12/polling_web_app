# Generated by Django 4.2.4 on 2023-09-01 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choices',
            old_name='choice_test',
            new_name='choice_text',
        ),
    ]
