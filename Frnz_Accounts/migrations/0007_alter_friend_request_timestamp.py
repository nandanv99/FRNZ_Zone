# Generated by Django 3.2.13 on 2022-06-20 12:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frnz_Accounts', '0006_auto_20220620_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend_request',
            name='timestamp',
            field=models.DateField(default=datetime.datetime(2022, 6, 20, 12, 52, 19, 699642)),
        ),
    ]
