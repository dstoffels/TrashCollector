# Generated by Django 3.2.5 on 2022-01-26 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='geolocation',
            field=models.CharField(default='', max_length=200),
        ),
    ]
