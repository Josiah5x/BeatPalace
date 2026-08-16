from django.urls import path

from .views import (
    dashboard,
    producer_dashboard,
    artist_dashboard
)


urlpatterns = [

    path(
        "",
        dashboard,
        name="dashboard"
    ),

    path(
        "producer/",
        producer_dashboard,
        name="producer_dashboard"
    ),

    path(
        "artist/",
        artist_dashboard,
        name="artist_dashboard"
    ),

]