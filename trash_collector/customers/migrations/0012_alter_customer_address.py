# Generated by Django 3.2.5 on 2022-01-27 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0011_auto_20220126_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=500),
        ),
    ]
