from django.db import models
from django.conf import settings


class ProducerProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="producer_profile",
    )

    # ==========================
    # BASIC INFORMATION
    # ==========================

    full_name = models.CharField(max_length=150, blank=True, default="")

    professional_title = models.CharField(
        max_length=150, default="Music Producer / Director"
    )

    profile_image = models.ImageField(
        upload_to="producers/profile/", blank=True, null=True
    )
    cover_image = models.ImageField(
        upload_to="producer/covers/",
        blank=True,
        null=True
    )

    bio = models.TextField(blank=True, null=True)

    # ==========================
    # EXPERIENCE PERIOD
    # ==========================

    start_year = models.PositiveIntegerField(blank=True, null=True)

    end_year = models.PositiveIntegerField(blank=True, null=True)

    # ==========================
    # CONTACT
    # ==========================

    phone = models.CharField(max_length=30, blank=True)

    email = models.EmailField(blank=True)

    instagram = models.CharField(max_length=100, blank=True)

    website = models.URLField(blank=True)

    # ==========================
    # SKILLS
    # ==========================

    skill_description = models.TextField(
        blank=True,
        help_text="Example: Music Composition, Audio Production & Sound Design",
    )

    # ==========================
    # SOFTWARE
    # ==========================

    software = models.TextField(
        blank=True, help_text="Example: Ableton Live, Cubase, Adobe Premiere, Logic Pro"
    )

    # ==========================
    # EDUCATION
    # ==========================

    education = models.TextField(blank=True)

    # ==========================
    # PERSONAL INFORMATION
    # ==========================

    date_of_birth = models.DateField(blank=True, null=True)

    marital_status = models.CharField(max_length=50, blank=True)

    # ==========================
    # STATUS
    # ==========================

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    @property
    def experience_years(self):

        if not self.start_year:
            return 0

        end_year = self.end_year

        if not end_year:
            from django.utils import timezone

            end_year = timezone.now().year

        return end_year - self.start_year

    @property
    def experience_period(self):

        if self.start_year and self.end_year:
            return f"{self.start_year}-{self.end_year}"

        if self.start_year:
            from django.utils import timezone

            return f"{self.start_year}-{timezone.now().year}"

        return ""


class ProducerProject(models.Model):

    PROJECT_TYPES = (
        ("produced", "Produced, Composed and Recorded"),
        ("directed", "Directed Music and Audio"),
    )

    producer = models.ForeignKey(
        ProducerProfile, on_delete=models.CASCADE, related_name="projects"
    )

    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES)

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    year = models.PositiveIntegerField(blank=True, null=True)

    display_order = models.PositiveIntegerField(default=0)

    is_visible = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "-year", "title"]

    def __str__(self):
        return self.title


class ProducerSkill(models.Model):

    producer = models.ForeignKey(
        ProducerProfile, on_delete=models.CASCADE, related_name="skills"
    )

    name = models.CharField(max_length=150)

    rating = models.PositiveIntegerField(default=1)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.name
