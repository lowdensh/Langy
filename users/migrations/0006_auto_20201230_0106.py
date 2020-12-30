# Generated by Django 3.1.1 on 2020-12-30 01:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20201230_0040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='join_date',
        ),
        migrations.AddField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
