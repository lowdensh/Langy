# Generated by Django 3.1.1 on 2021-01-19 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0013_auto_20201230_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learninglanguage',
            name='foreign_language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='language.foreignlanguage'),
        ),
    ]