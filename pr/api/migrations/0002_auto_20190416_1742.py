# Generated by Django 2.2 on 2019-04-16 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Status',
            new_name='ApplicationStatus',
        ),
    ]
