from django.urls import path

from .views import (
    artist_profile,
    edit_profile,
    public_artist_profile,
    discover_artists,
)


app_name = "artists"


urlpatterns = [

    # My profile
    path(
        "profile/",
        artist_profile,
        name="artist_profile",
    ),

    # Edit profile
    path(
        "profile/edit/",
        edit_profile,
        name="artist_edit_profile",
    ),

    # Discover artists
    path(
        "discover/",
        discover_artists,
        name="discover_artists",
    ),

    # Public artist profile
    path(
        "u/<str:username>/",
        public_artist_profile,
        name="public_artist_profile",
    ),

]