from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import RequestContext
from .forms import AdForm, CatForm, ProdForm, FeedForm, NameForm, LoginForm
from django.contrib.auth.decorators import login_required
from pymongo import MongoClient
import random, string, imghdr, datetime
from axes.decorators import watch_login
from bson.json_util import dumps
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.conf import settings as django_settings

import json, random, string, ast, os


# client = MongoClient('localhost', 27017)
# user_db= client.insale


client = MongoClient("mongodb://prince:princesharzeel@ds129143.mlab.com:29143/insale")
user_db = client.insale  # define database used


def home(request):
    ls = user_db.ads.find({"verified": "yes"}).sort([("time", -1)]).limit(5)
    return render(request, "index.html", {"result": ls})


def image(f, i):
    ext = imghdr.what(f)
    if ext in ["jpeg", "png", "bmp"]:
        a = "".join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            )
            for _ in range(3)
        )

        path = "static/media/" + i + "." + ext
        try:
            with open(path, "wb+") as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
        except:
            return "/static/media/default.jpg"
        return "/static/media/" + i + "." + ext
    else:
        return 0


def index(request):
    print("a")
    if request.method == "POST":
        print("b")
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            if "pica" in request.FILES:
                url = image(request.FILES["pica"], "pica" + request.POST["ftitle"])
                if url == 0:
                    messages.error(request, "Not an image")
                    return HttpResponseRedirect(request, "/login/")
                picture_a = url
            else:
                picture_a = "/static/media/default.jpg"

            if "picb" in request.FILES:
                url = image(request.FILES["picb"], "picb" + request.POST["ftitle"])
                if url == 0:
                    messages.error(request, "Not an image")
                    return HttpResponseRedirect(request, "/login/")
                picture_b = url
            else:
                picture_b = "/static/media/default.jpg"

            if "picc" in request.FILES:
                url = image(request.FILES["picc"], "picc" + request.POST["ftitle"])
                if url == 0:
                    messages.error(request, "Not an image")
                    return HttpResponseRedirect(request, "/login/")
                picture_c = url
            else:
                picture_c = "/static/media/default.jpg"

            print("c")
            name = form.cleaned_data["fname"]

            mobile = form.cleaned_data["fmobile"]
            email = form.cleaned_data["femail"]
            location = form.cleaned_data["flocation"]
            room = form.cleaned_data["froom"]
            title = form.cleaned_data["ftitle"]

            desc = form.cleaned_data["fdesc"]
            cat = form.cleaned_data["fcat"]
            price = form.cleaned_data["fprice"]
            date = form.cleaned_data["fdate"]

            timestamp = "{:%d-%b-%Y %H:%M:%S}".format(datetime.datetime.now())

            details = {
                "name": name,
                "mobile": mobile,
                "email": email,
                "location": location,
                "pica": picture_a,
                "picb": picture_b,
                "picc": picture_c,
                "time": timestamp,
                "room": room,
                "title": title,
                "desc": desc,
                "cat": cat,
                "price": price,
                "date": date,
                "verified": "no",
            }

            a = user_db.ads.find_one({"title": title})

            if a is not None:
                messages.error(request, "Select another title")
                return render(request, "post-ad.html")

            user_db.ads.insert(details)

            messages.success(request, "Product Added  for Verification by Admin")
            return HttpResponseRedirect("/")
        else:
            print(form.errors)
            messages.error(request, "Error in form filling")
            return render(request, "post-ad.html")

    form = AdForm()

    return render(request, "post-ad.html")


def prod_details(request, prod_name):
    title = prod_name
    a = user_db.ads.find_one({"title": title})
    details = {
        "name": a["name"],
        "mobile": a["mobile"],
        "email": a["email"],
        "pica": a["pica"],
        "picc": a["picc"],
        "picb": a["picb"],
        "date": a["date"],
        "time": a["time"],
        "location": a["location"],
        "room": a["room"],
        "title": a["title"],
        "desc": a["desc"],
        "cat": a["cat"],
        "price": a["price"],
    }

    return render(request, "single.html", {"form": details})


def category(request, catname):
    if catname == "All":
        a = user_db.ads.find({"verified": "yes"})
        form = CatForm()
        ls = user_db.ads.find({"verified": "yes"}, limit=5).sort([("time", -1)])
        return render(request, "cars.html", {"result": a, "latest": ls})

    a = user_db.ads.find({"cat": catname, "verified": "yes"})
    form = CatForm()
    ls = user_db.ads.find({"verified": "yes"}, limit=5).sort([("time", -1)])
    return render(request, "cars.html", {"result": a, "latest": ls})


def searchlist(request):
    if request.method == "POST":
        form = CatForm(request.POST)
        print(form.errors)
        if form.is_valid():
            loc = form.cleaned_data["location"]
            category = form.cleaned_data["category"]
            print(loc)
            print(category)

            latead = user_db.ads.find({"verified": "yes"}, limit=5).sort([("time", -1)])
            if loc == "All":
                if category == "All":
                    ls = user_db.ads.find({"verified": "yes"})

                    return render(
                        request, "cars.html", {"result": ls, "latest": latead}
                    )
                ls = user_db.ads.find({"cat": category, "verified": "yes"})
                print("category #####huru")
                return render(request, "cars.html", {"result": ls, "latest": latead})

            if category == "All":
                ls = user_db.ads.find({"location": loc, "verified": "yes"})
                return render(request, "cars.html", {"result": ls, "latest": latead})
            prods = user_db.ads.find({"cat": category, "location": loc})
            if prods is None:
                return HttpResponseRedirect("/list/All")
            return render(request, "cars.html", {"result": prods, "latest": latead})

    form = CatForm()

    return HttpResponseRedirect("/list/All")


def owner(request):
    tot = user_db.ads.find({}).count()

    verif_prod = user_db.ads.find({"verified": "yes"})
    revenue = 0
    for i in verif_prod:
        revenue = revenue + int(i["price"])

    ls = user_db.ads.find({"verified": "no"})
    counter = ls.count()

    print(revenue)
    return render(
        request,
        "dashboard.html",
        {"prods": ls, "revenue": revenue, "counter": counter, "total": tot},
    )


def product_update(request, prodname):

    if request.method == "POST":
        print("yes pressed it is")
        form = ProdForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["fname"]

            mobile = form.cleaned_data["fmobile"]
            email = form.cleaned_data["femail"]
            location = form.cleaned_data["flocation"]
            room = form.cleaned_data["froom"]
            title = form.cleaned_data["ftitle"]

            desc = form.cleaned_data["fdesc"]
            cat = form.cleaned_data["fcat"]
            price = form.cleaned_data["fprice"]
            date = form.cleaned_data["fdate"]
            details = {
                "name": name,
                "mobile": mobile,
                "email": email,
                "location": location,
                "room": room,
                "title": title,
                "desc": desc,
                "cat": cat,
                "price": price,
                "date": date,
            }

            a = user_db.ads.find_one({"title": prodname})

            user_db.ads.update_one(
                {"title": prodname},
                {
                    "$set": {
                        "name": name,
                        "mobile": mobile,
                        "email": email,
                        "location": location,
                        "room": room,
                        "title": title,
                        "desc": desc,
                        "cat": cat,
                        "price": price,
                        "date": date,
                    }
                },
                upsert=True,
            )

            messages.success(request, prodname + " Updated")
            return HttpResponseRedirect("/stock")
        else:
            print(form.errors)
            messages.error(request, "Error in form filling")
            return render(request, "user.html")

    form = ProdForm()
    a = user_db.ads.find_one({"title": prodname})
    print(a)
    details = {
        "name": a["name"],
        "mobile": a["mobile"],
        "email": a["email"],
        "location": a["location"],
        "pica": a["pica"],
        "picc": a["picc"],
        "picb": a["picb"],
        "pica": a["pica"],
        "picc": a["picc"],
        "picb": a["picb"],
        "room": a["room"],
        "title": a["title"],
        "desc": a["desc"],
        "cat": a["cat"],
        "price": a["price"],
        "date": a["date"],
    }
    print(details)

    return render(request, "user.html", {"prod": details})


def click_del(request, prodname):
    user_db.ads.remove({"title": prodname})
    return HttpResponseRedirect("/owner")


def verif(request, prodname):
    user_db.ads.update_one(
        {"title": prodname}, {"$set": {"verified": "yes"}}, upsert=True
    )
    return HttpResponseRedirect("/owner")


def rempic(request, pic):
    print(pic)
    a = user_db.ads.find_one({"pica": pic})
    b = user_db.ads.find_one({"picb": pic})
    c = user_db.ads.find_one({"picc": pic})
    if a is not None:
        user_db.ads.update_one(
            {"pica": pic}, {"$set": {"pica": "/static/media/default.jpg"}}, upsert=True
        )
        title = a["title"]

    if b is not None:
        user_db.ads.update_one(
            {"picb": pic}, {"$set": {"picb": "/static/media/default.jpg"}}, upsert=True
        )
        title = b["title"]

    if c is not None:
        user_db.ads.update_one(
            {"picc": pic}, {"$set": {"picc": "/static/media/default.jpg"}}, upsert=True
        )
        title = c["title"]
    return HttpResponseRedirect("/product/" + title)


from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

client_id = ""
client_secret = ""
redirect_uri = ""
if django_settings.DEBUG:
    redirect_uri = "http://localhost:8000/signup/"
fb_state = ""
# Create your views
def logfb(request):
    authorization_base_url = (
        "https://www.facebook.com/dialog/oauth/?scope=user_friends,email,public_profile"
    )
    token_url = "https://graph.facebook.com/oauth/access_token/"
    # redirect_uri = 'https://pacific-shelf-88987.herokuapp.com/redirect_facebook/'
    facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
    facebook = facebook_compliance_fix(facebook)
    authorization_url, state = facebook.authorization_url(authorization_base_url)
    return HttpResponseRedirect(authorization_url)


def signup(request):
    if request.method == "GET":
        try:
            code = request.GET["code"]
            request.session["code"] = code
            state = request.GET["state"]
        except Exception as e:
            print(e)
            return HttpResponseRedirect("/")
        else:
            if True:
                authorization_base_url = (
                    "https://www.facebook.com/dialog/oauth/?scope=email,public_profile"
                )
                token_url = "https://graph.facebook.com/oauth/access_token"

                facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
                facebook = facebook_compliance_fix(facebook)
                facebook.fetch_token(token_url, client_secret=client_secret, code=code)

                r3 = facebook.get(
                    "https://graph.facebook.com/v2.8/me/friends/?limit=500"
                )
                r2 = facebook.get(
                    "https://graph.facebook.com/v2.8/me?fields=id,name,email"
                )

                entry = json.loads(r3.content.decode("utf-8"))
                print(entry)
                try:
                    u = get_object_or_404(users, uid=entry["id"])
                    user = get_object_or_404(User, username=entry["id"])
                    try:
                        friends_raw = json.loads(r3.content.decode("utf-8"))
                    except Exception as e:
                        f = open(log_file, "a")
                        print(
                            str(getframeinfo(currentframe()).lineno) + " - " + str(e),
                            file=f,
                        )
                        f.close()
                        raise
                    u = get_object_or_404(users, uid=entry["id"])
                    flag = False
                    login(request, user)
                    u.picture = (
                        "https://graph.facebook.com/" + u.uid + "/picture?type=large"
                    )
                    u.save()
                    if not u.address_set.all().exists():
                        return HttpResponseRedirect("/additional-details")
                    return HttpResponseRedirect("/dashboard")
                except Exception as e:
                    if "email" not in entry:
                        entry["email"] = "example@eg.com"
                    entry1 = users(
                        name=entry["name"],
                        email=entry["email"],
                        uid=entry["id"],
                        picture="https://graph.facebook.com/"
                        + entry["id"]
                        + "/picture?type=large",
                    )
                    with transaction.atomic():
                        entry1.save()
                        User.objects.create_user(
                            username=entry["id"],
                            email=entry["email"],
                            password="".join(
                                random.SystemRandom().choice(
                                    string.ascii_uppercase
                                    + string.ascii_lowercase
                                    + string.digits
                                )
                                for _ in range(12)
                            ),
                        )

                # invitable_friends = []
                # invitable_friends_raw = json.loads(r1.content.decode("utf-8"))
                # for friend in invitable_friends_raw["data"]:
                #   invitable_friends.append(friend)

                friends_raw = json.loads(r3.content.decode("utf-8"))
                u = get_object_or_404(users, uid=entry["id"])
                flag = False
                for friend in friends_raw["data"]:
                    try:
                        u2 = get_object_or_404(users, uid=friend["id"])
                        u.primary.create(secondary=u2, level=2)
                        u2.primary.create(secondary=u, level=2)
                        flag = True
                    except Exception as e:
                        f = open(log_file, "a")
                        print(
                            str(getframeinfo(currentframe()).lineno) + " - " + str(e),
                            file=f,
                        )
                        f.close()
                        continue

                user = get_object_or_404(User, username=entry["id"])
                login(request, user)
                if flag:
                    return HttpResponseRedirect("/imported-contacts")
                else:
                    return HttpResponseRedirect("/additional-details")
            else:
                messages.add_message(request, messages.ERROR, "State Mismatch")
                return HttpResponseRedirect("/")


def stock(request):

    ls = user_db.ads.find({}).distinct("cat")
    mo = user_db.ads.find({"cat": "Mobiles", "verified": "yes"})
    fa = user_db.ads.find({"cat": "Fashion", "verified": "yes"})
    ex = user_db.ads.find({"cat": "Extras", "verified": "yes"})
    bsh = user_db.ads.find({"cat": "Books, Sports & hobbies", "verified": "yes"})
    ea = user_db.ads.find({"cat": "Electronics & Appliances", "verified": "yes"})

    fur = user_db.ads.find({"cat": "Furniture", "verified": "yes"})
    print(fa.count())

    return render(
        request,
        "stock.html",
        {"ls": ls, "mo": mo, "fa": fa, "ex": ex, "bsh": bsh, "ea": ea, "fur": fur},
    )


def feed(request):
    if request.method == "POST":
        print("yes pressed it is")
        form = FeedForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["fname"]

            lname = form.cleaned_data["flname"]
            email = form.cleaned_data["fmail"]
            feedback = form.cleaned_data["fmsg"]

            if len(feedback) != 0:
                print(feedback)
                try:
                    user_db.feed.insert(
                        {"name": name, "mail": email, "lname": lname, "msg": feedback}
                    )
                except:
                    messages.errors(request, "Error occured.Please try again later")
                    return HttpResponseRedirect("/feed")
                else:
                    messages.success(request, "Thanks for your feedback !!!")
                    return HttpResponseRedirect("/feed")
            else:
                messages.success(request, "Error occured.Empty Feedback")
                return HttpResponseRedirect("/feed")
    else:
        form = FeedForm()
        return render(request, "contact.html")


def feedview(request):
    feeds = user_db.feed.find({})
    return render(request, "table.html", {"feeds": feeds})


def namecont(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():

            latead = user_db.ads.find({"verified": "yes"}, limit=5).sort([("time", -1)])
            key = form.cleaned_data["fsearch"]

            ls = user_db.ads.find(
                {"verified": "yes", "title": {"$regex": key, "$options": "i"}}
            )
            if ls is None:
                return HttpResponseRedirect("/searchlist")
            return render(request, "cars.html", {"result": ls, "latest": latead})
        else:
            return HttpResponseRedirect("/searchlist")


def power(request):
    if request.method == "POST":
        l_form = LoginForm(request.POST)
        if l_form.is_valid():

            email = l_form.cleaned_data["fail"]
            psd = l_form.cleaned_data["fswd"]

            if email == "home@insale" and psd == "857414":
                return HttpResponseRedirect("/owner")
            else:
                messages.error(request, "Email or Password incorrect")
                return HttpResponseRedirect("/log")

        messages.error(request, "Fill the form correctly")
        return render(request, "log.html", {"l_form": l_form})
    l_form = LoginForm()
    return render(request, "log.html", {"l_form": l_form})
