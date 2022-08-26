# Generated by Django 4.1 on 2022-08-25 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("indoorGeolocation", "0005_alter_node_device"),
    ]

    operations = [
        migrations.AlterField(
            model_name="node",
            name="device",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="indoorGeolocation.device",
            ),
        ),
    ]