# Generated by Django 4.2.2 on 2023-07-05 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0002_goalcomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goalcomment',
            old_name='category',
            new_name='goal',
        ),
    ]