from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listings, Bids, Comments, Categories
from django import forms

from decimal import Decimal
import datetime 

# TODO: 
# display all categories
# display all listings according to a category


class Create_New(forms.Form):
    title = forms.CharField(label="Enter a title", max_length=30, min_length=5, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="Enter a description", max_length=50, min_length=5, widget=forms.TextInput(attrs={'class': 'form-control'}))
    starting_bid = forms.DecimalField(label="Enter a starting bid", min_value=Decimal(1), max_value=Decimal(599.99), decimal_places=2, 
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    # category = forms.ChoiceField(choices=categories, widget=forms.Select(attrs={'class': 'form-control'}))

class Bid(forms.Form):
    def __init__(self, *args, min_price, **kwargs):
        # `min_price` speichern und Konstruktor aufrufen
        super().__init__(*args, **kwargs)
        
        # Dynamisch das Feld `bid` erstellen
        self.fields['bid'] = forms.DecimalField(
            min_value=min_price,
            max_value=Decimal(999.99),
            initial=min_price,
            decimal_places=2,
            widget=forms.NumberInput(attrs={'class': 'form-control'})
        )

class Comment(forms.Form):
    comment = forms.CharField(label="Comment: ", max_length=100, min_length=5, widget=forms.Textarea(attrs={'class': 'form-control'}))


def index(request):
    listings = list(Listings.objects.filter(active=True))
    results = []
    
    for listing in listings:
        bids = listing.bids.all().order_by('-price')

        # search bids on listing
        if bids.count() == 0:
            price = listing.starting_bid
        else:
            price = bids.first().price

        results.append((listing, price))

    return render(request, "auctions/index.html", {
        'results': results, 'title': 'Active Listings'
    })

@login_required(login_url='login')
def watchlist(request):
    if request.method == "POST":
        form = request.POST["watchlist"]
        listing_id = request.POST["listing_id"]
        listing = Listings.objects.get(pk=listing_id)
        user = request.user

        if form == "add":
            user.watchlist.add(listing)
        else:
            user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing.user.username, listing_id)))
    else:
        listings = list(request.user.watchlist.all())
        results = []
        
        for listing in listings:
            bids = listing.bids.all().order_by('-price')

            # search bids on listing
            if bids.count() == 0:
                price = listing.starting_bid
            else:
                price = bids.first().price

            results.append((listing, price))

        return render(request, "auctions/index.html", {
            'results': results, 'title': 'Marked Listings'
        })


def category(request, category):
    if category == "all":
        objects = Categories.objects.all()
        categories = []
        for object in objects:
            info = (object.name, object.listings.filter(active=True).count())
            categories.append(info)
            
        return render(request, "auctions/category.html", {
            'categories': categories, 'title': 'Categories'
        })
    
    else:
        try:
            object = Categories.objects.get(name=category)
        except Categories.DoesNotExist:
            return HttpResponseRedirect(reverse("category", args=['all']))   
        
        listings = list(object.listings.filter(active=True))
        results = []
        
        for listing in listings:
            bids = listing.bids.all().order_by('-price')

            # search bids on listing
            if bids.count() == 0:
                price = listing.starting_bid
            else:
                price = bids.first().price

            results.append((listing, price))

        return render(request, "auctions/index.html", {
            'results': results, 'title': category
        })


def listing(request, username, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)

        # If creator of listing
        if request.user.username == username:
            form = request.POST["auction"]

            if form == "close":
                listing.end_date = datetime.date.today()
                listing.active = False
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=(username, listing_id)))     

        # Else: user places bid on listing
        else: 
            # search bids on listing
            bids = listing.bids.all()
            if bids.count() == 0:
                price = listing.starting_bid
            else:
                price = bids.first().price
            
            min_price = price + Decimal("0.01")
            form = Bid(request.POST, min_price=min_price)

            if form.is_valid() and request.user.is_authenticated:
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

            # Else: invalid input
            else:
                form.fields["bid"].widget.attrs["class"] += " is-invalid"
                form.fields["bid"].widget.attrs["aria-describedby"] = "invalid_bid"
                return render(request, "auctions/listing.html", {
                    'listing': listing, 'bid_form': form, 'bids': bids, 'highest_bid': price, 'comment_form': Comment(), 'comments': listing.comments.all()
                }) 

    else:
        # Render listing with form min_price above all bids 
        listing = Listings.objects.get(pk=listing_id)
        if listing.user.username == username: 
            bids = listing.bids.all().order_by('-price')

            if bids.count() == 0:
                price = listing.starting_bid
            else:
                price = bids.first().price
            
            min_price = price + Decimal("0.01")
            bid_form = Bid(min_price=min_price) 

            return render(request, "auctions/listing.html", {
                'listing': listing, 'bid_form': bid_form, 'bids': bids, 'highest_bid': price, 'comment_form': Comment(), 'comments': listing.comments.all()
            })
        
        # If url not correct <user>/<listing_id>
        else:
            return HttpResponseRedirect(reverse("index")) 
        

def comment(request, username, listing_id):
    if request.method == "POST":
        form = Comment(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            comment = Comments(
                user=request.user,
                listing=Listings.objects.get(pk=listing_id),
                comment=form.cleaned_data["comment"]
            )
            comment.save()
            return HttpResponseRedirect(reverse("listing", args=(username, listing_id)))    
        
        # Render comment form again
        else:
            listing = Listings.objects.get(pk=listing_id)
            bids = listing.bids.all().order_by('-price')

            if bids.count() == 0:
                price = listing.starting_bid
            else:
                price = bids.first().price
            
            min_price = price + Decimal("0.01")
            bid_form = Bid(min_price=min_price) 
            return render(request, "auctions/listing.html", {
                'listing': listing, 'bid_form': bid_form, 'bids': bids, 'highest_bid': price, 'comment_form': form, 'comments': listing.comments.all()
            })
    else:
        pass

 

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
                starting_bid=Decimal(listing["starting_bid"]), 
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
