# /accounts/login/
# /accounts/register/
# /accounts/logout/

from django.urls import path
from . import views

urlpatterns = [
    path("/accounts/login/", views.Index, name="login"),
    path("/accounts/register/", views.Index, name="register"),
    path("/accounts/logout/", views.Index, name="logout"),

]