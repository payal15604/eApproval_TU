# Generated by Django 4.2.16 on 2024-11-24 10:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_alter_nodueslip_roll_no_alter_nodueslip_room_no"),
    ]

    operations = [
        migrations.AddField(
            model_name="lorrequest",
            name="request_status",
            field=models.CharField(default="Pending", max_length=20),
        ),
        migrations.AddField(
            model_name="nocrequest",
            name="request_status",
            field=models.CharField(default="Pending", max_length=20),
        ),
        migrations.AddField(
            model_name="nodueslip",
            name="request_status",
            field=models.CharField(default="Pending", max_length=20),
        ),
    ]
