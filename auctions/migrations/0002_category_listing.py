# Generated by Django 4.0 on 2021-12-28 16:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(max_length=500, null=True)),
                ('startingbid', models.FloatField()),
                ('currentbid', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateField(default=datetime.datetime.now)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auctions.user')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='similar_listings', to='auctions.category')),
                ('creater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_creaters_lists', to='auctions.user')),
                ('watcher', models.ManyToManyField(blank=True, related_name='watched_listing', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
