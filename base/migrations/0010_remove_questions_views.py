# Generated by Django 3.2.21 on 2024-01-08 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20240108_0829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questions',
            name='views',
        ),
    ]
