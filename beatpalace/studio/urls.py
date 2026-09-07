from django.urls import path
from . import views

app_name = "studio"

urlpatterns = [

    # Owner management FIRST
    path(
        "owner/",
        views.owner_dashboard,
        name="owner_dashboard",
    ),

    path(
        "owner/studios/",
        views.my_studios,
        name="my_studios",
    ),

    path(
        "owner/studios/create/",
        views.create_studio,
        name="create_studio",
    ),

    path(
        "owner/studios/<int:studio_id>/",
        views.studio_owner_detail,
        name="studio_owner_detail",
    ),

    path(
        "owner/studios/<int:studio_id>/workspaces/create/",
        views.create_workspace,
        name="create_workspace",
    ),

    # Public
    path(
        "",
        views.studio_list,
        name="studio_list",
    ),

    path(
        "<int:studio_id>/",
        views.studio_detail,
        name="studio_detail",
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


    path(
    "owner/studios/<int:studio_id>/services/create/",
    views.create_service,
    name="create_service",
    ),

    path(
    "owner/services/<int:service_id>/edit/",
    views.edit_service,
    name="edit_service",
    ),

    path(
    "owner/services/<int:service_id>/delete/",
    views.delete_service,
    name="delete_service",
    ),

    path(
    "owner/bookings/<int:booking_id>/confirm/",
    views.confirm_booking,
    name="confirm_booking",
    ),

    path(
        "owner/bookings/<int:booking_id>/reject/",
        views.reject_booking,
        name="reject_booking",
    ),

    path(
        "owner/bookings/<int:booking_id>/start/",
        views.start_booking,
        name="start_booking",
    ),

    path(
        "owner/bookings/<int:booking_id>/complete/",
        views.complete_booking,
        name="complete_booking",
    ),
]