from django.urls import path

from . import views


app_name = "messaging"


urlpatterns = [

    path(
        "chat/<int:collaboration_id>/",
        views.chat,
        name="chat",
    ),

]