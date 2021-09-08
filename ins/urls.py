from django.conf.urls import url
from django.contrib import admin
from ins import views

urlpatterns = [
    url(r"^$", views.index, name="post"),
    url(r"^owner/$", views.owner, name="owner"),
    url(r"^single/(?P<prod_name>[\w|\W]+)/$", views.prod_details, name="single"),
    url(r"^home/$", views.home, name="home"),
    url(r"^list/(?P<catname>[\w|\W]+)/$", views.category, name="category"),
    url(r"^searchlist/$", views.searchlist, name="searchlist"),
    url(r"^product/(?P<prodname>[\w|\W]+)/$", views.product_update, name="prodate"),
    url(r"^del/(?P<prodname>[\w|\W]+)/$", views.click_del, name="del"),
    url(r"^rempic/(?P<pic>[\w|\W]+)/$", views.rempic, name="rempic"),
    url(r"^verif/(?P<prodname>[\w|\W]+)/$", views.verif, name="verif"),
    url(r"^signup/$", views.signup, name="signup"),
    url(r"^stock/$", views.stock, name="stock"),
    url(r"^feed/$", views.feed, name="feed"),
    url(r"^feedview/$", views.feedview, name="feedview"),
    url(r"^name/$", views.namecont, name="cont"),
    url(r"^log/$", views.power, name="log"),
    url(r"^logfb/$", views.logfb, name="logfb"),
]
