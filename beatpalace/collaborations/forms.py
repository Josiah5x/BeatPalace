from django import forms
from .models import Collaboration


class CollaborationRequestForm(forms.ModelForm):

    class Meta:
        model = Collaboration

        fields = [
            "message",
        ]

        widgets = {
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": (
                        "Tell the producer what you would "
                        "like to collaborate on..."
                    ),
                }
            ),
        }