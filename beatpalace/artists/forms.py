from django import forms

from .models import ArtistProfile


class ArtistProfileForm(forms.ModelForm):

    class Meta:

        model = ArtistProfile

        fields = [
            "artist_name",
            "bio",
            "avatar",
            "cover_image",
            "genre",
            "location",
            "website",
            "instagram",
            "twitter",
        ]

        widgets = {

            "artist_name": forms.TextInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "Your artist name",
                }
            ),

            "bio": forms.Textarea(
                attrs={
                    "class": "form-controls form-control",
                    "rows": 5,
                    "placeholder": "Tell people about yourself...",
                }
            ),

            "genre": forms.TextInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "Afrobeats, Hip Hop, R&B...",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "Abuja, Nigeria",
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "https://...",
                }
            ),

            "instagram": forms.URLInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "Instagram URL",
                }
            ),

            "twitter": forms.URLInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "X/Twitter URL",
                }
            ),
        }