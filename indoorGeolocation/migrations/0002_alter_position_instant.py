# Generated by Django 4.0.3 on 2022-07-11 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indoorGeolocation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='instant',
            field=models.DateTimeField(auto_now=True),
        ),
    ]