# Generated by Django 4.0 on 2022-01-04 13:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_rename_bid_offer_bid_bid_alter_bid_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='auctions',
            new_name='auction',
        ),
        migrations.AlterField(
            model_name='bid',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 4, 13, 47, 11, 166899)),
        ),
    ]
