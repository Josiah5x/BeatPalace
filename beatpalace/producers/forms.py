from django import forms

from .models import ProducerProfile


class ProducerProfileForm(forms.ModelForm):

    class Meta:

        model = ProducerProfile

        fields = [
            "stage_name",
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

            "stage_name": forms.TextInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "Your producer name",
                }
            ),

            "bio": forms.Textarea(
                attrs={
                    "class": "form-controls form-control",
                    "rows": 5,
                    "placeholder": "Tell artists about yourself...",
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
                    "placeholder": "Lagos, Nigeria",
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