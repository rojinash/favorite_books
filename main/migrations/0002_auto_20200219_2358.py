# Generated by Django 2.2 on 2020-02-19 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='passsword',
            new_name='password',
        ),
    ]
