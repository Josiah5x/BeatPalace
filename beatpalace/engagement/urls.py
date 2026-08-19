from django.urls import path

from . import views


urlpatterns = [

    path(
        "follow/<int:user_id>/",
        views.toggle_follow,
        name="toggle_follow"
    ),

]