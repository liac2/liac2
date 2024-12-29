from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listings, Bids
from django import forms

from decimal import Decimal


categories = [("", "Select category"), ("G", "Games"), ("O", "Other")]

class Create_New(forms.Form):
    title = forms.CharField(label="Enter a title", max_length=30, min_length=5)
    description = forms.CharField(label="Enter a description", max_length=50, min_length=5)
    starting_bid = forms.DecimalField(label="Enter a starting bid", min_value=1, max_value=999.99, decimal_places=2)
    url = forms.URLField(required=False)
    category = forms.ChoiceField(choices=categories)

class Bid(forms.Form):
    bid = forms.DecimalField(min_value=1, max_value=999.99, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    

# Custom function
# def errror(request, msg):
#     return render(request, "auctions/error.html", {
#         'error_msg': msg
#     })

def index(request):
    listings = list(Listings.objects.all())
    results = []
    
    for index, listing in enumerate(listings):
        bids = listing.bids.all().order_by('-price')

        try:
            price = bids[0].price
        except IndexError:
            price = listing.starting_bid

        results.append((listing, price))

    return render(request, "auctions/index.html", {
        'listings': listings, 'results': results
    })

@login_required(login_url='login')
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
        form = Bid(request.POST)

        if form.is_valid():
            # TODO
            """ For validations: https://getbootstrap.com/docs/5.3/forms/validation/#server-side"""

            # Add bid to db
            price = form.cleaned_data["bid"]
            bid = Bids(
                user=request.user,
                listing=listing,
                price=price
            )
            bid.save()
            listing.bids.add(bid)       
            return HttpResponseRedirect(reverse("listing", args=(username, listing_id)))
            

        else:
            form.fields["bid"].widget.attrs["class"] += " is-invalid"
            form.fields["bid"].widget.attrs["aria-describedby"] = "invalid_bid"
            return render(request, "auctions/listing.html", {
                'listing': listing, 'bid_form': form
            }) 
            
    else:

        # Render listing with form min_price above all bids 
        listing = Listings.objects.get(pk=listing_id)
        bids = listing.bids.all().order_by('-price')
        bid_form = Bid()

        if len(bids) == 0:
            price = listing.starting_bid
        else:
            price = bids[0].price

        bid_form.fields["bid"].min_value = price + Decimal("0.01")
        bid_form.fields['bid'].initial = price + Decimal("0.01")

        return render(request, "auctions/listing.html", {
            'listing': listing, 'bid_form': bid_form, 'bids': bids, 'highest_bid': price
        })

@login_required(login_url='login')
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
