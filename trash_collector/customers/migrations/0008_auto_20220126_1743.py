# Generated by Django 3.2.5 on 2022-01-26 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_auto_20220126_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='lat',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='lng',
            field=models.CharField(default=0, max_length=50),
        ),
    ]