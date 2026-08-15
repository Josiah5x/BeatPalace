# /messages/
# /messages/<username>/

from django.urls import path
from . import views

urlpatterns = [
    path("/messages/", views.Index, name="message"),
    path("/messages/<username>", views.Index, name="message_username"),

]