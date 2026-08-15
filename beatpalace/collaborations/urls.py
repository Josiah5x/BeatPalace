# /collaborations/
# /collaborations/create/

from django.urls import path
from . import views

urlpatterns = [
    path("/collaborations/", views.Index, name="collaboration"),
    path("/collaborations/create/", views.Index, name="collaborations_create"),

]