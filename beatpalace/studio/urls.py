from django.urls import path
from . import views

app_name = "studio"

urlpatterns = [
    # Public
    path("", views.studio_list, name="studio_list"),
    path("<int:studio_id>/", views.studio_detail, name="studio_detail"),

    # Owner
    path("owner/", views.owner_dashboard, name="owner_dashboard"),
    path("owner/studios/", views.my_studios, name="my_studios"),
    path("owner/studios/create/", views.create_studio, name="create_studio"),

    path(
        "owner/studios/<int:studio_id>/",
        views.studio_detail_owner,
        name="studio_owner_detail",
    ),

    path(
        "owner/studios/<int:studio_id>/workspaces/create/",
        views.create_workspace,
        name="create_workspace",
    ),

    # Booking
    path(
        "<int:studio_id>/book/",
        views.create_booking,
        name="create_booking",
    ),

    path(
        "bookings/<int:booking_id>/",
        views.booking_detail,
        name="booking_detail",
    ),
]