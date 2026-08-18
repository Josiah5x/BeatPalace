from django.urls import path

from .views import (
    producer_profile,
    edit_profile,
)


urlpatterns = [

    path(
        "profile/edit/",
        edit_profile,
        name="producer_edit_profile"
    ),

    path(
        "<str:username>/",
        producer_profile,
        name="producer_profile"
    ),


]