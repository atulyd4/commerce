# Generated by Django 4.0 on 2022-01-05 08:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_listing_activate_alter_bid_created_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='activate',
            new_name='active',
        ),
        migrations.AlterField(
            model_name='bid',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 5, 8, 19, 33, 936886)),
        ),
    ]
