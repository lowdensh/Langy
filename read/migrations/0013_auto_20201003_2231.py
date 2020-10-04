# Generated by Django 3.1.1 on 2020-10-03 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0012_author_other_names'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='website',
        ),
        migrations.AddField(
            model_name='book',
            name='website',
            field=models.URLField(default='default'),
            preserve_default=False,
        ),
    ]
