# Generated by Django 4.0 on 2022-01-01 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_listing_buyer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='alt',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='listing',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_picture', to='auctions.listing'),
        ),
    ]
