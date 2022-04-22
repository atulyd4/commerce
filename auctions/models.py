from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import TextField
from django.db.models.fields.related import create_many_to_many_intermediary_model
from datetime import datetime, timezone


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.id}: {self.category}'


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, max_length=500)
    active = models.BooleanField(default=True)
    startingbid = models.FloatField()
    currentbid = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default="No category yet!", related_name="similar_listings")
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="all_creaters_lists")
    watcher = models.ManyToManyField(
        User, blank=True, related_name="watched_listing")
    buyer = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    created_at = models.DateField(default=datetime.now)

    def __str__(self):
        return f'{self.id} : {self.title}'

    @property
    def first_picture(self):
        return self.pictures.first().picture.url


class Picture(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="pictures", blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to='images/')
    alt = models.CharField(null=True, max_length=100)


class Bid(models.Model):
    auction = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now)


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(default=datetime.now())
