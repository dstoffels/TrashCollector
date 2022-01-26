# Generated by Django 3.2.5 on 2022-01-26 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_customer_geolocation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='geolocation',
        ),
        migrations.AddField(
            model_name='customer',
            name='lat',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='lng',
            field=models.CharField(default='', max_length=50),
        ),
    ]
