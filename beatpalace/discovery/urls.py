from django.urls import path
from . import views

app_name = "discover"


urlpatterns = [

    path(
        "",
        views.discover_home,
        name="discover"
    ),

    path(
        "artists/",
        views.discover_artists,
        name="discover_artists"
    ),

    path(
        "producers/",
        views.discover_producers,
        name="discover_producers"
    ),

]