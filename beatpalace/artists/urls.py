from django.urls import path

from .views import (
    artist_profile,
    edit_profile,
)


urlpatterns = [

    path(
        "profile/edit/",
        edit_profile,
        name="artist_edit_profile"
    ),

    path(
        "<str:username>/",
        artist_profile,
        name="artist_profile"
    ),

]