from django.contrib.auth.models import AbstractUser
from django.db import models


categories = [("G", "Games"), ("O", "Other")]

class User(AbstractUser):
    pass


# auction listings
class Listings(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    starting_bid = models.DecimalField(max_digits=5, decimal_places=2)
    url = models.URLField()
    category = models.CharField(max_length=3, choices=categories, default="O", blank=True, null=True)



# # bids
# class Bids(models.Model):
#     pass

# # comments made on auction listings
# class Comments(models.Model):
#     pass
