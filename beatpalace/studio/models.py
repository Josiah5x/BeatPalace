from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Studio(models.Model):

    STUDIO_TYPES = [
        ("recording", "Recording Studio"),
        ("mixing", "Mixing Room"),
        ("production", "Production Room"),
        ("rehearsal", "Rehearsal Room"),
        ("podcast", "Podcast / Video Studio"),
        ("content", "Content Creation Space"),
    ]

    STATE = [
        ("Abia",     "Abia"),
        ("Adamawa",     "Adamawa"),
        ("Akwa Ibom",     "Akwa Ibom"),
        ("Anambra",     "Anambra"),
        ("Bauchi",     "Bauchi"),
        ("Bayelsa",     "Bayelsa"),
        ("Benue",     "Benue"),
        ("Borno",     "Borno"),
        ("Cross River",     "Cross River"),
        ("Delta",     "Delta"),
        ("Ebonyi",     "Ebonyi"),
        ("Edo",     "Edo"),
        ("Ekiti",     "Ekiti"),
        ("Enugu",     "Enugu"),
        ("FCT - Abuja",     "FCT - Abuja"),
        ("Gombe",     "Gombe"),
        ("Imo",     "Imo"),
        ("Jigawa",     "Jigawa"),
        ("Kaduna",     "Kaduna"),
        ("Kano",     "Kano"),
        ("Katsina",     "Katsina"),
        ("Kebbi",     "Kebbi"),
        ("Kogi",     "Kogi"),
        ("Kwara",     "Kwara"),
        ("Lagos",     "Lagos"),
        ("Nasarawa",     "Nasarawa"),
        ("Niger",     "Niger"),
        ("Ogun",     "Ogun"),
        ("Ondo",     "Ondo"),
        ("Osun",     "Osun"),
        ("Oyo",     "Oyo"),
        ("Plateau",     "Plateau"),
        ("Rivers",     "Rivers"),
        ("Sokoto",     "Sokoto"),
        ("Taraba",     "Taraba"),
        ("Yobe",     "Yobe"),
        ("Zamfara",     "Zamfara"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_studios",
    )

    name = models.CharField(max_length=200)

    studio_type = models.CharField(
        max_length=30,
        choices=STUDIO_TYPES,
        default="recording",
    )

    description = models.TextField()

    address = models.CharField(
        max_length=255,
    )

    city = models.CharField(
        max_length=100,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        choices=STATE,
    )

    country = models.CharField(
        max_length=100,
        default="Nigeria",
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    hourly_rate = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )

    daily_rate = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )

    capacity = models.PositiveIntegerField(
        default=5,
    )

    equipment = models.TextField(
        blank=True,
        help_text="List studio equipment and instruments.",
    )

    amenities = models.TextField(
        blank=True,
    )

    rules = models.TextField(
        blank=True,
    )

    cover_image = models.ImageField(
        upload_to="studios/covers/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class StudioImage(models.Model):

    studio = models.ForeignKey(
        Studio,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="studios/gallery/",
    )

    caption = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.studio.name} Image"


class Workspace(models.Model):

    studio = models.ForeignKey(
        Studio,
        on_delete=models.CASCADE,
        related_name="workspaces",
    )

    name = models.CharField(
        max_length=150,
    )

    description = models.TextField(
        blank=True,
    )

    hourly_rate = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )

    capacity = models.PositiveIntegerField(
        default=2,
    )

    equipment = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.studio.name} - {self.name}"


class StudioService(models.Model):

    studio = models.ForeignKey(
        Studio,
        on_delete=models.CASCADE,
        related_name="services",
    )

    name = models.CharField(
        max_length=150,
    )

    description = models.TextField(
        blank=True,
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )

    price_type = models.CharField(
        max_length=20,
        choices=[
            ("fixed", "Fixed Price"),
            ("hourly", "Per Hour"),
        ],
        default="fixed",
    )

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.name


class StudioBooking(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("in_session", "In Session"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("rejected", "Rejected"),
    ]

    BOOKING_TYPES = [
        ("hourly", "Hourly"),
        ("daily", "Daily"),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="studio_bookings",
    )

    studio = models.ForeignKey(
        Studio,
        on_delete=models.PROTECT,
        related_name="bookings",
    )

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.PROTECT,
        related_name="bookings",
        null=True,
        blank=True,
    )

    booking_type = models.CharField(
        max_length=20,
        choices=BOOKING_TYPES,
        default="hourly",
    )

    booking_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    number_of_people = models.PositiveIntegerField(
        default=1,
    )

    notes = models.TextField(
        blank=True,
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    service_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-booking_date", "-start_time"]

    def __str__(self):
        return (
            f"{self.customer} - "
            f"{self.studio.name} - "
            f"{self.booking_date}"
        )

    @property
    def duration_hours(self):
        """
        Calculate booking duration in hours.
        """
        start = timezone.datetime.combine(
            self.booking_date,
            self.start_time,
        )

        end = timezone.datetime.combine(
            self.booking_date,
            self.end_time,
        )

        seconds = (end - start).total_seconds()

        return Decimal(str(seconds / 3600))
    def overlaps_existing_booking(self):
        """
        Check whether this booking overlaps another active booking
        for the same workspace.
        """

        if not self.workspace:
            return False

        return StudioBooking.objects.filter(
            workspace=self.workspace,
            booking_date=self.booking_date,
            status__in=[
                "pending",
                "confirmed",
                "in_session",
            ],
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(
            pk=self.pk
        ).exists()




class BookingService(models.Model):

    booking = models.ForeignKey(
        StudioBooking,
        on_delete=models.CASCADE,
        related_name="booking_services",
    )

    service = models.ForeignKey(
        StudioService,
        on_delete=models.PROTECT,
        related_name="booking_items",
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.service.name} - {self.booking}"



class StudioPayment(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    booking = models.OneToOneField(
        StudioBooking,
        on_delete=models.CASCADE,
        related_name="payment",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    reference = models.CharField(
        max_length=200,
        unique=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.reference


