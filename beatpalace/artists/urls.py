from django.urls import path

from .views import (
    artist_profile,
    public_artist_profile,
    edit_profile,
)


urlpatterns = [

    path(
        "profile/",
        artist_profile,
        name="artist_profile"
    ),
    path(
        "profile/edit/",
        edit_profile,
        name="artist_edit_profile"
    ),

      # Logged-in artist's own profile
    path(
        "profile/",
        artist_profile,
        name="artist_profile",
    ),

    # Public artist profile
    path(
        "u/<str:username>/",
        public_artist_profile,
        name="public_artist_profile",
    ),

]