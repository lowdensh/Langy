# Generated by Django 3.1.1 on 2020-12-20 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['surname', 'forename', 'other_names']},
        ),
        migrations.RenameField(
            model_name='book',
            old_name='source_URL',
            new_name='source_url',
        ),
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='book_covers', verbose_name='Book Cover'),
        ),
        migrations.AddField(
            model_name='book',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='book_pdfs', verbose_name='Book PDF'),
        ),
        migrations.AlterField(
            model_name='page',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='read.book'),
        ),
    ]
