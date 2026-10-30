from django.urls import path

from . import views


app_name = "collaborations"


urlpatterns = [

    path(
        "send/<str:username>/",
        views.send_collaboration,
        name="send_collaboration",
    ),
    path(
        "accept/<str:pk>/",
        views.accept_collaboration,
        name="accept_collaboration",
    ),
    path(
        "send/<str:pk>/",
        views.reject_collaboration,
        name="reject_collaboration",
    ),

    path(
        "requests/",
        views.collaboration_requests,
        name="requests",
    ),

    path(
        "requests/<int:collaboration_id>/<str:action>/",
        views.respond_collaboration,
        name="respond_collaboration",
    ),

    path(
        "workspace/<int:collaboration_id>/",
        views.collaboration_workspace,
        name="workspace",
    ),

    path(
    "workspace/<int:collaboration_id>/",
    views.collaboration_workspace,
    name="workspace",
    ),

]