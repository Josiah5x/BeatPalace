from django.contrib import admin

from .models import (
    Studio,
    StudioImage,
    Workspace,
    StudioService,
    StudioBooking,
    BookingService,
    StudioPayment,
)


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "owner",
        "studio_type",
        "city",
        "hourly_rate",
        "is_active",
        "created_at",
    )

    list_filter = (
        "studio_type",
        "city",
        "is_active",
    )

    search_fields = (
        "name",
        "owner__username",
        "city",
    )


@admin.register(StudioImage)
class StudioImageAdmin(admin.ModelAdmin):

    list_display = (
        "studio",
        "caption",
        "created_at",
    )


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "studio",
        "hourly_rate",
        "capacity",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "studio__name",
    )


@admin.register(StudioService)
class StudioServiceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "studio",
        "price",
        "price_type",
        "is_active",
    )

    list_filter = (
        "price_type",
        "is_active",
    )


@admin.register(StudioBooking)
class StudioBookingAdmin(admin.ModelAdmin):

    list_display = (
        "studio",
        "workspace",
        "customer",
        "booking_date",
        "start_time",
        "end_time",
        "total_amount",
        "status",
    )

    list_filter = (
        "status",
        "booking_type",
        "booking_date",
    )

    search_fields = (
        "studio__name",
        "customer__username",
    )


@admin.register(BookingService)
class BookingServiceAdmin(admin.ModelAdmin):

    list_display = (
        "booking",
        "service",
        "quantity",
        "price",
        "total",
    )


@admin.register(StudioPayment)
class StudioPaymentAdmin(admin.ModelAdmin):

    list_display = (
        "booking",
        "amount",
        "reference",
        "status",
        "paid_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "reference",
    )