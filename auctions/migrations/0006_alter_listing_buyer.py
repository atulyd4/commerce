# Generated by Django 4.0 on 2021-12-31 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_rename_creater_listing_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='auctions.user'),
        ),
    ]
