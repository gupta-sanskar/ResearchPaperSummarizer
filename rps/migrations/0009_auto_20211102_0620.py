# Generated by Django 3.2.8 on 2021-11-02 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rps', '0008_message_room'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
    ]