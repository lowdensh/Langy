# Generated by Django 3.1.1 on 2020-12-22 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0010_auto_20201222_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(default='default.jpg', upload_to='book_covers'),
        ),
    ]
