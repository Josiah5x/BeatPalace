from django import forms

from .models import ArtistProfile


class ArtistProfileForm(forms.ModelForm):

    class Meta:

        model = ArtistProfile

        fields = [

            # Basic
            "artist_name",
            "bio",
            "avatar",
            "cover_image",

            # Music
            "genre",
            "location",

            # Contact
            "phone",
            "email",

            # Social
            "instagram",
            "twitter",
            "website",

            # Professional
            "start_year",
            "end_year",
            "skill_description",
            "education",

            # Personal
            "date_of_birth",
            "marital_status",

            # Statistics
            "monthly_listeners",

            # Profile
            "is_published",
        ]

        widgets = {

            # ==========================================
            # BASIC INFORMATION
            # ==========================================

            "artist_name": forms.TextInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "Artist Name",
                }
            ),

            "bio": forms.Textarea(
                attrs={
                    "class": "form-controls form-control",
                    "rows": 5,
                    "placeholder": (
                        "Tell people about yourself, "
                        "your music and your artistic journey..."
                    ),
                }
            ),

            "avatar": forms.ClearableFileInput(
                attrs={
                    "class": "form-controls form-control",
                    "accept": "image/*",
                }
            ),

            "cover_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-controls form-control",
                    "accept": "image/*",
                }
            ),

            # ==========================================
            # MUSIC
            # ==========================================

            "genre": forms.TextInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": (
                        "Afrobeats, Hip-Hop, R&B..."
                    ),
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "Abuja, Nigeria",
                }
            ),

            # ==========================================
            # CONTACT
            # ==========================================

            "phone": forms.TextInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "+234...",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "artist@example.com",
                }
            ),

            # ==========================================
            # SOCIAL
            # ==========================================

            "instagram": forms.URLInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": (
                        "https://instagram.com/username"
                    ),
                }
            ),

            "twitter": forms.URLInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": (
                        "https://x.com/username"
                    ),
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": (
                        "https://example.com"
                    ),
                }
            ),

            # ==========================================
            # PROFESSIONAL
            # ==========================================

            "start_year": forms.NumberInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "2018",
                    "min": 1900,
                }
            ),

            "end_year": forms.NumberInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "Present",
                }
            ),

            "skill_description": forms.Textarea(
                attrs={
                    "class": "form-controls form-control",
                    "rows": 3,
                    "placeholder": (
                        "Songwriting, Vocal Performance, "
                        "Music Composition..."
                    ),
                }
            ),

            "education": forms.Textarea(
                attrs={
                    "class": "form-controls form-control",
                    "rows": 4,
                    "placeholder": (
                        "Educational and musical background"
                    ),
                }
            ),

            # ==========================================
            # PERSONAL
            # ==========================================

            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "form-controls form-control",
                    "type": "date",
                }
            ),

            "marital_status": forms.TextInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "Marital Status",
                }
            ),

            # ==========================================
            # STATISTICS
            # ==========================================

            "monthly_listeners": forms.NumberInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "0",
                    "min": 0,
                }
            ),

            # ==========================================
            # PROFILE STATUS
            # ==========================================

            "is_published": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }