# Generated by Django 4.1.5 on 2023-02-15 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_items'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Items',
            new_name='Item',
        ),
    ]