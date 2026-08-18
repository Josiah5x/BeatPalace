from django.urls import path

from . import views


urlpatterns = [

    path(
        "upload/",
        views.upload_music,
        name="upload_music"
    ),

    path(
    "my-music/",
    views.my_music,
    name="my_music"
),

]