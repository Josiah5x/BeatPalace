from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from functools import wraps
from django.contrib import messages
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import (
    Studio,
    StudioBooking,
    StudioService,
    Workspace,
    BookingService,
)

from .forms import (
    StudioForm,
    WorkspaceForm,
    StudioBookingForm,
    StudioServiceForm,
)


def producer_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):

        # Admin can access everything
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        # Only producers can manage studios
        if getattr(request.user, "role", None) != "producer":
            raise PermissionDenied(
                "Only producers can manage studios."
            )

        return view_func(request, *args, **kwargs)

    return wrapper

@producer_required
def create_studio(request):

    if request.method == "POST":

        form = StudioForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            studio = form.save(
                commit=False
            )

            studio.owner = request.user

            studio.save()

            return redirect(
                "studio:studio_owner_detail",
                studio_id=studio.id,
            )

    else:

        form = StudioForm()

    return render(
        request,
        "studio/create_studio.html",
        {
            "form": form,
        },
    )


@producer_required
def owner_dashboard(request):
    studios = Studio.objects.filter(
        owner=request.user
    )

    bookings = StudioBooking.objects.filter(
        studio__owner=request.user
    ).select_related(
        "studio",
        "workspace",
        "customer",
    )

    context = {
        "studios": studios,
        "bookings": bookings[:10],
        "total_studios": studios.count(),
        "total_bookings": bookings.count(),
        "pending_bookings": bookings.filter(
            status="pending"
        ).count(),
        "confirmed_bookings": bookings.filter(
            status="confirmed"
        ).count(),
    }

    return render(
        request,
        "studio/owner_dashboard.html",
        context,
    )


@producer_required
def my_studios(request):
    studios = Studio.objects.filter(
        owner=request.user
    )

    return render(
        request,
        "studio/my_studio.html",
        {"studios": studios},
    )


@producer_required
def studio_owner_detail(request, studio_id):

    studio = get_object_or_404(
        Studio,
        id=studio_id,
        owner=request.user,
    )

    workspaces = studio.workspaces.all()

    services = studio.services.all()

    bookings = (
        studio.bookings
        .select_related(
            "customer",
            "workspace",
        )
        .order_by(
            "-booking_date",
            "-start_time",
        )
    )

    return render(
        request,
        "studio/studio_owner_detail.html",
        {
            "studio": studio,
            "workspaces": workspaces,
            "services": services,
            "bookings": bookings,
        },
    )



@producer_required
def create_workspace(request, studio_id):

    studio = get_object_or_404(
        Studio,
        id=studio_id,
        owner=request.user,
    )

    if request.method == "POST":

        form = WorkspaceForm(request.POST)

        if form.is_valid():

            workspace = form.save(commit=False)

            workspace.studio = studio

            workspace.save()

            messages.success(
                request,
                "Workspace created successfully."
            )

            return redirect(
                "studio:studio_owner_detail",
                studio_id=studio.id,
            )

    else:

        form = WorkspaceForm()

    return render(
        request,
        "studio/create_workspace.html",
        {
            "form": form,
            "studio": studio,
        },
    )


@producer_required
def create_booking(request, studio_id):

    studio = get_object_or_404(
        Studio,
        id=studio_id,
        is_active=True,
    )

    if request.method == "POST":

        form = StudioBookingForm(
            request.POST,
            studio=studio,
        )

        if form.is_valid():

            with transaction.atomic():

                booking = form.save(
                    commit=False
                )

                booking.customer = request.user
                booking.studio = studio
                booking.booking_type = "hourly"

                workspace = booking.workspace

                duration = booking.duration_hours

                if workspace:

                    booking.subtotal = (
                        workspace.hourly_rate
                        * duration
                    )

                else:

                    booking.subtotal = (
                        studio.hourly_rate
                        * duration
                    )

                selected_services = (
                    form.cleaned_data.get(
                        "services"
                    )
                )

                service_total = Decimal("0.00")

                booking.save()

                for service in selected_services:

                    if service.price_type == "hourly":

                        service_total += (
                            service.price
                            * duration
                        )

                    else:

                        service_total += service.price

                    BookingService.objects.create(

                        booking=booking,

                        service=service,

                        quantity=1,

                        price=service.price,

                        total=(
                            service.price
                            * duration
                            if service.price_type == "hourly"
                            else service.price
                        ),
                    )

                booking.service_fee = service_total

                booking.total_amount = (
                    booking.subtotal
                    + booking.service_fee
                )

                booking.save()

            messages.success(
                request,
                "Your studio booking has been submitted."
            )

            return redirect(
                "studio:booking_detail",
                booking_id=booking.id,
            )

    else:

        form = StudioBookingForm(
            studio=studio
        )

    return render(
        request,
        "studio/create_booking.html",
        {
            "studio": studio,
            "form": form,
        },
    )



@login_required
def booking_detail(request, booking_id):

    booking = get_object_or_404(
        StudioBooking.objects.select_related(
            "studio",
            "workspace",
            "customer",
        ).prefetch_related(
            "booking_services__service"
        ),
        id=booking_id,
    )

    if (
        booking.customer != request.user
        and booking.studio.owner != request.user
    ):
        return redirect(
            "studio:owner_dashboard"
        )

    return render(
        request,
        "studio/booking_detail.html",
        {
            "booking": booking,
        },
    )


def studio_list(request):

    studios = (
        Studio.objects
        .filter(is_active=True)
        .select_related("owner")
        .prefetch_related("images", "workspaces")
    )

    city = request.GET.get("city")
    studio_type = request.GET.get("type")
    search = request.GET.get("q")

    if city:
        studios = studios.filter(city__icontains=city)

    if studio_type:
        studios = studios.filter(
            studio_type=studio_type
        )

    if search:
        studios = studios.filter(
            name__icontains=search
        )

    context = {
        "studios": studios,
        "studio_types": Studio.STUDIO_TYPES,
        "selected_city": city or "",
        "selected_type": studio_type or "",
        "search": search or "",
    }

    return render(
        request,
        "studio/studio_list.html",
        context,
    )





def studio_detail(request, studio_id):
    studio = get_object_or_404(
        Studio.objects
        .filter(is_active=True)
        .select_related("owner")
        .prefetch_related("images", "workspaces", "services"),
        id=studio_id,
    )

    workspaces = studio.workspaces.filter(is_active=True)
    services = studio.services.filter(is_active=True)

    return render(
        request,
        "studio/studio_detail.html",
        {
            "studio": studio,
            "workspaces": workspaces,
            "services": services,
        },
    )




@producer_required
def create_service(request, studio_id):

    studio = get_object_or_404(
        Studio,
        id=studio_id,
        owner=request.user,
    )

    if request.method == "POST":

        form = StudioServiceForm(request.POST)

        if form.is_valid():

            service = form.save(commit=False)

            service.studio = studio

            service.save()

            messages.success(
                request,
                f"{service.name} has been added successfully."
            )

            return redirect(
                "studio:studio_owner_detail",
                studio_id=studio.id,
            )

    else:

        form = StudioServiceForm()

    return render(
        request,
        "studio/create_service.html",
        {
            "form": form,
            "studio": studio,
        },
    )



@producer_required
def edit_service(request, service_id):

    service = get_object_or_404(
        StudioService,
        id=service_id,
        studio__owner=request.user,
    )

    studio = service.studio

    if request.method == "POST":

        form = StudioServiceForm(
            request.POST,
            instance=service,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                f"{service.name} has been updated."
            )

            return redirect(
                "studio:studio_owner_detail",
                studio_id=studio.id,
            )

    else:

        form = StudioServiceForm(
            instance=service
        )

    return render(
        request,
        "studio/edit_service.html",
        {
            "form": form,
            "service": service,
            "studio": studio,
        },
    )



@producer_required
def delete_service(request, service_id):

    service = get_object_or_404(
        StudioService,
        id=service_id,
        studio__owner=request.user,
    )

    studio_id = service.studio.id

    if request.method == "POST":

        service_name = service.name

        service.delete()

        messages.success(
            request,
            f"{service_name} has been deleted."
        )

    return redirect(
        "studio:studio_owner_detail",
        studio_id=studio_id,
    )

@producer_required
def confirm_booking(request, booking_id):

    booking = get_object_or_404(
        StudioBooking,
        id=booking_id,
        studio__owner=request.user,
    )

    if request.method == "POST":

        if booking.status != "pending":

            messages.warning(
                request,
                "Only pending bookings can be confirmed."
            )

        elif booking.overlaps_existing_booking():

            messages.error(
                request,
                "This workspace is already booked during this time."
            )

        else:

            booking.status = "confirmed"

            booking.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            messages.success(
                request,
                "Booking confirmed successfully."
            )

    return redirect(
        "studio:booking_detail",
        booking_id=booking.id,
    )



@producer_required
def reject_booking(request, booking_id):

    booking = get_object_or_404(
        StudioBooking,
        id=booking_id,
        studio__owner=request.user,
    )

    if request.method == "POST":

        if booking.status != "pending":

            messages.warning(
                request,
                "Only pending bookings can be rejected."
            )

        else:

            booking.status = "rejected"

            booking.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            messages.success(
                request,
                "Booking rejected."
            )

    return redirect(
        "studio:booking_detail",
        booking_id=booking.id,
    )


@producer_required
def start_booking(request, booking_id):

    booking = get_object_or_404(
        StudioBooking,
        id=booking_id,
        studio__owner=request.user,
    )

    if request.method == "POST":

        if booking.status != "confirmed":

            messages.warning(
                request,
                "Only confirmed bookings can be started."
            )

        else:

            booking.status = "in_session"

            booking.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            messages.success(
                request,
                "Booking session has started."
            )

    return redirect(
        "studio:booking_detail",
        booking_id=booking.id,
    )



@producer_required
def complete_booking(request, booking_id):

    booking = get_object_or_404(
        StudioBooking,
        id=booking_id,
        studio__owner=request.user,
    )

    if request.method == "POST":

        if booking.status != "in_session":

            messages.warning(
                request,
                "Only active sessions can be completed."
            )

        else:

            booking.status = "completed"

            booking.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            messages.success(
                request,
                "Booking has been completed."
            )

    return redirect(
        "studio:booking_detail",
        booking_id=booking.id,
    )






