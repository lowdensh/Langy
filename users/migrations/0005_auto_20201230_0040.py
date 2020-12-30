# Generated by Django 3.1.1 on 2020-12-30 00:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201111_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='date_joined',
        ),
        migrations.AddField(
            model_name='customuser',
            name='join_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date joined'),
            preserve_default=False,
        ),
    ]
