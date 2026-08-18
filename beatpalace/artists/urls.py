from django.urls import path

from .views import (
    artist_profile,
    edit_profile,
    artist_dashboard,
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

    path(
    "dashboard/",
    artist_dashboard,
    name="artist_dashboard"
),

]