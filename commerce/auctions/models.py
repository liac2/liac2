from django.contrib.auth.models import AbstractUser
from django.db import models


categories = [("G", "Games"), ("O", "Other")]

class User(AbstractUser):
    watchlist = models.ManyToManyField("Listings", blank=True, related_name="users")


# auction listings
class Listings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_listings")
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    starting_bid = models.DecimalField(max_digits=5, decimal_places=2)
    url = models.URLField()
    category = models.CharField(max_length=3, choices=categories, default="O", blank=True, null=True)


# bids
class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(max_digits=5, decimal_places=2)


# # comments made on auction listings
# class Comments(models.Model):
#     pass
