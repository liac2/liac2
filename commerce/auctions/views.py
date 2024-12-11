from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Categories, Listings, Bids, Comments
from django import forms

attributes = ["title", "description", "starting_bid", "url", "category"]
categories = [("T", "Trex")]
# for category in Categories.objects.all():
#     categories.append((category.pk, category.category))

class Create_New(forms.Form):
    title = forms.CharField(label="Enter a title", max_length=30, min_length=10)
    description = forms.CharField(label="Enter a description", max_length=50, min_length=10)
    starting_bid = forms.DecimalField(label="Enter a starting bid", min_value=1, max_value=999.99, decimal_places=2)
    url = forms.URLField(initial="https://", help_text="This is a help_text")
    category = forms.ChoiceField(choices=categories)

def index(request):
    return render(request, "auctions/index.html")


def create(request):
    if request.method == "POST":
        form = Create_New(request.POST)
        if form.is_valid():

            # Get all data
            listing = {}
            for attribute in attributes:
                listing[attribute] = form.cleaned_data[attribute]
            
            # Input data into database
            

            return
            
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
