# Generated by Django 3.2.21 on 2024-01-07 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='active',
        ),
    ]
