# Generated by Django 3.1.1 on 2021-02-15 21:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0036_learningtracking_learning_language'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracking', '0002_auto_20210215_2126'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Session',
            new_name='LangySession',
        ),
    ]
