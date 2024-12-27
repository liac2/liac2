from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings
from django import forms


categories = [("", "Select category"), ("G", "Games"), ("O", "Other")]

class Create_New(forms.Form):
    title = forms.CharField(label="Enter a title", max_length=30, min_length=5)
    description = forms.CharField(label="Enter a description", max_length=50, min_length=5)
    starting_bid = forms.DecimalField(label="Enter a starting bid", min_value=1, max_value=999.99, decimal_places=2)
    url = forms.URLField(required=False)
    category = forms.ChoiceField(choices=categories)

class Bid(forms.Form):
    bid = forms.DecimalField(min_value=1, max_value=999.99, decimal_places=2, widget=)
    

def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listings.objects.all()
    })

# - [ ] if authenticated: add/remove to watch list

def watchlist(request):
    if request.method == "POST":
        form = request.POST["watchlist"]
        listing_id = request.POST["listing_id"]
        listing = Listings.objects.get(pk=listing_id)
        user = User.objects.get(pk=request.user.id)

        if form == "add":
            user.watchlist.add(listing)
        else:
            user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing.user.username, listing_id)))
    else:
        pass


def listing(request, username, listing_id):
    if request.method == "POST":
        # search bids on listing
        listing = Listings.objects.get(pk=listing_id)
        bids = listing.bids.all()
        return HttpResponseRedirect(reverse("listing", args=(username, listing_id)))
        

    else:
        return render(request, "auctions/listing.html", {
            'listing': Listings.objects.get(pk=listing_id), 'bid_form': Bid()
        })


def create(request):
    if request.method == "POST":
        form = Create_New(request.POST)
        if form.is_valid():

            # Get all data
            listing = form.cleaned_data
            
            # Input data into database
            new = Listings(
                user=request.user, 
                title=listing["title"], 
                description=listing["description"], 
                starting_bid=listing["starting_bid"], 
                url=listing["url"],
                category=listing["category"]
            )
            new.save()

            return HttpResponseRedirect(reverse("index"))
            
        # Else: INVALID
        return render(request, "auctions/create.html", {
            "new_form": form
        })

    
    # If GET
    else:
        return render(request, "auctions/create.html", {
            "new_form": Create_New()
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
