# Generated by Django 3.1.1 on 2020-11-11 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0003_auto_20201111_2216'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='WordCategory',
        ),
    ]