# Generated by Django 3.2.8 on 2021-10-24 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rps', '0002_alter_file_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]