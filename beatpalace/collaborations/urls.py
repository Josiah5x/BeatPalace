from django.urls import path

from . import views


app_name = "collaborations"


urlpatterns = [

    path(
    "",
    views.collaboration_dashboard,
    name="collaboration_dashboard",
    ),

    path(
        "u/<str:username>/",
        views.send_collaboration,
        name="send_collaboration",
    ),

    path(
        "requests/",
        views.collaboration_requests,
        name="requests",
    ),

    path(
        "<int:pk>/accept/",
        views.accept_collaboration,
        name="accept_collaboration",
    ),

    path(
        "<int:pk>/reject/",
        views.reject_collaboration,
        name="reject_collaboration",
    ),

    path(
        "<int:pk>/cancel/",
        views.cancel_collaboration,
        name="cancel_collaboration",
    ),

]