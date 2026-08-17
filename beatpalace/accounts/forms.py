from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "role",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Normal form fields
        for name, field in self.fields.items():

            if name == "role":
                # Radio buttons
                field.widget.attrs.update({
                    "class": "form-check-input"
                })

            else:
                # Text, email and password fields
                field.widget.attrs.update({
                    "class": "form-controls form-control"
                })


        # Placeholders
        self.fields["username"].widget.attrs.update({
            "placeholder": "Enter username"
        })

        self.fields["email"].widget.attrs.update({
            "placeholder": "Enter email address"
        })

        self.fields["password1"].widget.attrs.update({
            "placeholder": "Enter password"
        })

        self.fields["password2"].widget.attrs.update({
            "placeholder": "Confirm password"
        })