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

def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listings.objects.all()
    })


def listing(request, username, listing_id):
    pass


def create(request):
    if request.method == "POST":
        form = Create_New(request.POST)
        if form.is_valid():

            # Get all data
            listing = form.cleaned_data
            
            # Input data into database
            new = Listings(
                user_id=request.user, 
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
