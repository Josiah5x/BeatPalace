from django.urls import path

from .views import send_collaboration


app_name = "collaborations"


urlpatterns = [

    path(
        "send/<str:username>/",
        send_collaboration,
        name="send_collaboration",
    ),

]