# Generated by Django 3.2.8 on 2021-10-26 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rps', '0004_rename_file_pdffile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdffile',
            name='file',
        ),
        migrations.AddField(
            model_name='pdffile',
            name='summary',
            field=models.TextField(default=''),
        ),
    ]
