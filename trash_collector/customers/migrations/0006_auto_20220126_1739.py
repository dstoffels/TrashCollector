# Generated by Django 3.2.5 on 2022-01-26 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_auto_20220126_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='lng',
        ),
    ]
