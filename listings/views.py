from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
import logging

import stripe

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, ListItem, Comment, Bid

def sellerIndex(request):
    items = ListItem.objects.filter(active=True)
    return render(request, "listings/sellerIndex.html", {
        "heading" : "Active Requests",
        "items" : items
    })

def index(request):
    #items = ListItem.objects.filter(active=True)
    items = ListItem.objects.filter(creator=request.user)
    return render(request, "listings/index.html", {
        "heading" : "Your requested items",
        "items" : items
    })



def inactive(request):
    items = ListItem.objects.filter(active=False)
    return render(request, "listings/index.html", {
        "heading" : "Inactive Listings",
        "items" : items
    })

def all(request):
    #items = ListItem.objects.all()
    items = ListItem.objects.filter(creator=request.user)
    return render(request, "listings/index.html", {
        "heading" : "Your requested items",
        "items" : items
    })
def sellerAll(request):
    #items = ListItem.objects.all()
    items = ListItem.objects.filter(active=True)
    return render(request, "listings/sellerIndex.html", {
        "heading" : "Active Requests",
        "items" : items
    })

@login_required(login_url="login")
def watchlist(request):
    user = User.objects.get(username = request.user)
    items = user.user_watchlist.all()
    return render(request, "listings/index.html", {
        "heading" : "Your Watchlist",
        "items" : items
    })

def categories(request):
    categories = ListItem.CATEGORIES
    return render(request, "listings/categories.html", {
        "categories" : categories
    })

def category(request, category):
    items = ListItem.objects.filter(category = category, active=True)
    return render(request, "listings/index.html", {
        "heading" : f"Active Listings - ({category})",
        "items" : items
    })

def about(request):
    return render(request, "listings/about.html")

def my_listings(request):
    items = ListItem.objects.filter(creator=request.user)
    return render(request, "listings/index.html", {
        "heading" : "Your Listings",
        "items" : items
    })

def wins(request):
    #logging.basicConfig(level=logging.INFO)
    #logger = logging.getLogger('myapp')
    #logger.info(request.user)
    temps = ListItem.objects.filter(active=False)
    items_ids = []
    for temp in temps:
        bids = temp.item.all().order_by('bid')
        if bids:
            highestbid = bids.first()
            if str(highestbid.bidder.username) == str(request.user):
                items_ids.append(temp.id)
    items = ListItem.objects.filter(pk__in = items_ids)
    return render(request, "listings/sellerIndex.html", {
        "heading" : "Confirmed Deals",
        "items" : items
    })

@login_required(login_url="login")
def new(request):
    if request.method == "POST":
        new_item = ListItem()
        new_item.active = True
        new_item.title = request.POST["title"]
       
        new_item.description = request.POST["description"]
        new_item.reserve_price = request.POST["reserve_price"]
        #new_item.reserve_price=0
        new_item.current_price = request.POST["reserve_price"]

        new_item.contact = request.POST["contact"]
        new_item.category = request.POST["category"]
        new_item.creator = request.user
        if "image" in request.FILES:
            new_item.image = request.FILES["image"]
        new_item.save()
        return redirect("item", item_id=new_item.id)
    else:
        return render(request, "listings/new.html")

def item(request, item_id):
    item = ListItem.objects.get(id = item_id)
    bids = item.item.all().order_by('bid')
    comments = item.listing.all()
    watchlist_button = None
    color = None
    next_bid = None
    winner = bids.first()
    if winner:
        winner = winner.bidder.username
    if item.active:
        price_tag = "Current Price Offered"
        style = None
    else:
        price_tag = "Confirmed at"
        style = "filter: blur(1px); opacity: 0.7;"

    if request.user.is_authenticated:
        temp = item.watchlist.filter(username = request.user)

        if request.method == "GET" and "watch" in request.GET:
            user = User.objects.get(username= request.user)
            if temp:
                user.user_watchlist.remove(item)
            else:
                user.user_watchlist.add(item)
            temp = item.watchlist.filter(username = request.user)

        if temp :
            watchlist_button = "-"
            color = "#ff2020"
        else:
            watchlist_button = "+"
            color = "#15ff00"

        # if bids:
        #     next_bid = int(item.current_price + item.current_price/10)
        # else:
        #     next_bid = item.reserve_price


    return render(request, "listings/item.html", {
        "item" : item,
        "button" : watchlist_button,
        "buttoncolor" : color,
        "nxt_bid" : next_bid,
        "bids" : bids,
        "price_tag" : price_tag,
        "style" : style,
        "winner" : winner,
        "comments" : comments
    })


def sellerItem(request, item_id):
    item = ListItem.objects.get(id = item_id)
    bids = item.item.all().order_by('bid')
    comments = item.listing.all()
    
    watchlist_button = None
    color = None
    next_bid = None
    winner = bids.first()
    if winner:
        winner = winner.bidder.username
        #winner = winner.item.title
    if item.active:
        price_tag = "Current Price Offered"
        style = None
    else:
        price_tag = "Confirmed at"
        style = "filter: blur(1px); opacity: 0.7;"

    if request.user.is_authenticated:
        temp = item.watchlist.filter(username = request.user)

        if request.method == "GET" and "watch" in request.GET:
            user = User.objects.get(username= request.user)
            if temp:
                user.user_watchlist.remove(item)
            else:
                user.user_watchlist.add(item)
            temp = item.watchlist.filter(username = request.user)

        if temp :
            watchlist_button = "-"
            color = "#ff2020"
        else:
            watchlist_button = "+"
            color = "#15ff00"

        # if bids:
        #     next_bid = int(item.current_price + item.current_price/10)
        # else:
        #     next_bid = item.reserve_price


    return render(request, "listings/sellerItem.html", {
        "item" : item,
        "button" : watchlist_button,
        "buttoncolor" : color,
        "nxt_bid" : next_bid,
        "bids" : bids,
        "price_tag" : price_tag,
        "style" : style,
        "winner" : winner,
        "comments" : comments
    })

def close(request, item_id):
    item = ListItem.objects.get(id = item_id)
    item.active = False
    global temp_item_id
    temp_item_id=item_id
    item.save()
    return redirect("item", item_id=item_id)

@login_required(login_url="login")
def bid(request, item_id):
    item = ListItem.objects.get(id = item_id)
    user = User.objects.get(username= request.user)

    if request.method == "POST":
        bid = Bid()
        bid.item = item
        bid.bidder = user
        bid.bid = request.POST["bid"]
        bid.save()

        item.current_price = request.POST["bid"]
        item.save()
        #User.objects.filter(username=user).get(GST=t)
        if(int(bid.bid)<350):
        #logging.basicConfig(level=logging.INFO)
        #logger = logging.getLogger('myapp')
        #User.objects
            User.objects.filter(username=user).update(prediction="Fraud")
    return redirect("sellerItem", item_id=item_id)

top_price=1000
temp_item_id=0
@login_required(login_url="login")
def checkcurr(request, item_id):
    # return redirect("item", item_id=item_id)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('myapp')
    item = ListItem.objects.get(id = item_id)
    user = User.objects.get(username= request.user)
    if request.method == "POST":
        bid = Bid()
        bid.item = item
        bid.bidder = user
        logger.info(request.POST["checks"])
        bid.bid = request.POST["checks"]
        # bid.save()
        #logging.basicConfig(level=logging.INFO)
        #logger = logging.getLogger('myapp')
        item.current_price = request.POST["checks"]
        global top_price 
        top_price = int(item.current_price)
        #logger.info(item.current_price)
        item.save()

    close(request, item_id=item_id)
    
    #return redirect("item", item_id=item_id)
    return render(request, "checkout.html")


def completeOrder(request):
    return redirect("item", item_id=temp_item_id)

@login_required(login_url="login")
def comment(request, item_id):
    if request.method == "POST":
        item = ListItem.objects.get(id = item_id)
        user = User.objects.get(username= request.user)
        comment = Comment()
        comment.item = item
        comment.which_user = user
        comment.comment = request.POST["comment"]
        comment.save()
    return redirect("item", item_id=item_id)

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
            return render(request, "listings/login.html", {
                "message": "*Invalid username and/or password."
            })
    elif "next" in request.GET and request.GET["next"] == "/new/":
            return render(request, "listings/login.html", {
                "message": "*LogIn is required to create new listing"
            })
    else:
        return render(request, "listings/login.html")
def loginSeller(request):
    if request.method == "POST":
    #if True:
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("sellerIndex"))

        else:

            return render(request, "listings/loginSeller.html", {
                "message": "*Invalid username and/or password."
            })
    elif "next" in request.GET and request.GET["next"] == "/new/":
            return render(request, "listings/loginSeller.html", {
                "message": "*LogIn is required to create new listing"
            })
    else:
        return render(request, "listings/loginSeller.html")


def logout_view(request):
    logout(request)
    return render(request, "listings/login.html", {
        "message": "*You have successfully logged out."
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "listings/register.html", {
                "message": "*Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "listings/register.html", {
                "message": "*Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "listings/register.html")

def registerSeller(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        GST1=request.POST["GST"]

        temp=GST1[0:2]
        l=len(GST1)
        temp1=GST1[l-2]

        ans=0

        if(l==15 and temp.isnumeric() and temp1=='Z'):
            ans=1
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "listings/registerSeller.html", {
                "message": "*Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            if ans==1:
                User.objects.filter(username=username).update(GST=GST1)
            else :
                User.objects.filter(username=username).update(GST="Invalid")


        except IntegrityError:
            return render(request, "listings/registerSeller.html", {
                "message": "*Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("sellerIndex"))
    else:
        return render(request, "listings/registerSeller.html")


#payment


stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'

@csrf_exempt
def create_checkout_session(request):
 session = stripe.checkout.Session.create(
 payment_method_types=['card'],
 line_items=[{
 'price_data': {
 'currency': 'inr',
 'product_data': {
 'name': 'Total Amount',
 },
 'unit_amount': top_price *100,
 },
 'quantity': 1,
 }],
 mode='payment',
 success_url=YOUR_DOMAIN + '/success.html',
 cancel_url=YOUR_DOMAIN + '/cancel.html',
 )
 return JsonResponse({'id': session.id})

def home(request):
 return render(request,'checkout.html')

#success view
def success(request):
 return render(request,'success.html')

 #cancel view
def cancel(request):
 return render(request,'cancel.html')