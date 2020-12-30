# Generated by Django 3.1.1 on 2020-12-29 20:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('language', '0010_auto_20201229_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learninglanguage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learning', to=settings.AUTH_USER_MODEL),
        ),
    ]
