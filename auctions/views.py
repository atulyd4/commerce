from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import fields
from django.db.models.fields import TextField
from django.forms import widgets
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Bid, Category, Comment, Picture, User, Listing
from django import forms
from django.contrib import messages


class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "startingbid", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "startingbid": forms.NumberInput(attrs={"class": "form-control"}),
        }


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ["picture", "alt"]
        widgets = {
            "alt": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "alt_text"}
            ),
        }


class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid"]
        widgets = {
            "bid": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Bid"}
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                }
            )
        }


def index(request):
    listings = Listing.objects.exclude(active=False)
    return render(request, "auctions/index.html", {"listings": listings})


@login_required
def listing_details(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comment_data = listing.comments.all()
    return render(
        request,
        "auctions/details.html",
        {
            "listing": listing,
            "bid_form": NewBidForm(),
            "comment_data": comment_data,
            "comment_form": CommentForm(),
        },
    )


def Add_comment(request, listing_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        newform = form.save(commit=False)
        newform.listing_id = listing_id
        newform.user = request.user
        newform.save()
        return HttpResponseRedirect(reverse("index"))


def add_watchlist(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    listing.watcher.add(request.user)
    return HttpResponseRedirect(reverse("index"))


def remove_watchlist(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    listing.watcher.remove(request.user)
    return HttpResponseRedirect(reverse("watchistlindex"))


@login_required
def watchlist_index(request):
    watchlist = Listing.objects.filter(watcher=request.user)
    return render(request, "auctions/watchlist.html", {"watchlists": watchlist})


def category_view(request):
    categories = Category.objects.all()
    return render(request, "auctions/category.html", {"categories": categories})


def category_listing(request, category_id):
    cat = Category.objects.filter(id=category_id).first()
    listings = cat.similar_listings.exclude(active=False)
    return render(request, "auctions/index.html", {"listings": listings})


@login_required
def take_bid(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    bid_form = NewBidForm(request.POST)
    bid_form.is_valid()
    bid = bid_form.cleaned_data["bid"]
    if is_valid(bid, listing):
        listing.currentbid = bid
        form = NewBidForm(request.POST)
        newbid = form.save(commit=False)
        newbid.auction = listing
        newbid.user = request.user
        newbid.save()
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        bid_form.add_error(
            "bid",
            f"bid amount should be greater than { listing.startingbid if  listing.currentbid == None else listing.currentbid}",
        )
        return render(
            request, "auctions/details.html", {"listing": listing, "bid_form": bid_form}
        )


def is_valid(bid, listing):
    if bid >= (listing.startingbid) and (
        listing.currentbid is None or bid > listing.currentbid
    ):
        return True
    else:
        return False


def close_listing(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    latest = None
    try:
        latest = listing.bids.latest("bid")
    except:
        pass

    if request.user == listing.creator:
        listing.active = False
        listing.buyer = request.user if latest is None else latest.user
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        listing.watcher.add(request.user)
        return HttpResponseRedirect(reverse("details"))


def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        img_form = PictureForm(request.POST, request.FILES)
        if form.is_valid() and img_form.is_valid():
            newlisting = form.save(commit=False)
            newlisting.creator = request.user
            newlisting.save()

            picture = img_form.cleaned_data["picture"]
            alt_text = img_form.cleaned_data["alt"]
            newpicture = Picture(listing=newlisting, picture=picture, alt=alt_text)
            newpicture.save()
            return HttpResponseRedirect(reverse("index"))

    return render(
        request,
        "auctions/newlist.html",
        {"form": NewListingForm(), "img_form": PictureForm()},
    )


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
