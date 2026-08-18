from django import forms
from .models import Music


class MusicUploadForm(forms.ModelForm):

    class Meta:
        model = Music

        fields = [
            "title",
            "music_type",
            "genre",
            "description",
            "audio_file",
            "artwork",
            "is_public",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "Enter music title",
                }
            ),

            "music_type": forms.Select(
                attrs={
                    "class": "form-select form-controls",
                }
            ),

            "genre": forms.Select(
                attrs={
                    "class": "form-select form-controls",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-controls form-control",
                    "rows": 4,
                    "placeholder": "Describe your music...",
                }
            ),

            "audio_file": forms.FileInput(
                attrs={
                    "class": "form-controls form-control",
                    "accept": "audio/*",
                }
            ),

            "artwork": forms.FileInput(
                attrs={
                    "class": "form-controls form-control",
                    "accept": "image/*",
                }
            ),

            "is_public": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }