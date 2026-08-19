from django import forms

from .models import (
    ProducerProfile,
    ProducerProject,
    ProducerSkill,
)


class ProducerProfileForm(forms.ModelForm):

    class Meta:

        model = ProducerProfile

        fields = [
            "full_name",
            "professional_title",
            "profile_image",
            "bio",
            "start_year",
            "end_year",
            "phone",
            "email",
            "instagram",
            "website",
            "skill_description",
            "software",
            "education",
            "date_of_birth",
            "marital_status",
            "is_published",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-controls form-control", "placeholder": "Full Name"}
            ),
            "professional_title": forms.TextInput(
                attrs={
                    "class": "form-controls form-control",
                    "placeholder": "Music Producer / Director",
                }
            ),
            "profile_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-controls form-control",
                    "rows": 4,
                    "placeholder": "Tell people about yourself...",
                }
            ),
            "start_year": forms.NumberInput(
                attrs={"class": "form-controls form-control", "placeholder": "2018"}
            ),
            "end_year": forms.NumberInput(
                attrs={"class": "form-controls form-control", "placeholder": "2025"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-controls form-control", "placeholder": "+234..."}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-controls form-control", "placeholder": "email@example.com"}
            ),
            "instagram": forms.TextInput(
                attrs={"class": "form-controls form-control", "placeholder": "@username"}
            ),
            "website": forms.URLInput(
                attrs={"class": "form-controls form-control", "placeholder": "https://example.com"}
            ),
            "skill_description": forms.Textarea(
                attrs={
                    "class": "form-controls form-control",
                    "rows": 3,
                    "placeholder": "Music Composition, Audio Production & Sound Design",
                }
            ),
            "software": forms.Textarea(
                attrs={
                    "class": "form-controls form-control",
                    "rows": 3,
                    "placeholder": "Ableton Live, Cubase, Logic Pro...",
                }
            ),
            "education": forms.Textarea(
                attrs={
                    "class": "form-controls form-control",
                    "rows": 4,
                    "placeholder": "Educational background",
                }
            ),
            "date_of_birth": forms.DateInput(
                attrs={"class": "form-controls form-control", "type": "date"}
            ),
            "marital_status": forms.TextInput(
                attrs={"class": "form-controls form-control", "placeholder": "Marital Status"}
            ),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ProducerProjectForm(forms.ModelForm):

    class Meta:

        model = ProducerProject

        fields = [
            "project_type",
            "title",
            "description",
            "year",
            "display_order",
            "is_visible",
        ]

        widgets = {
            "project_type": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(
                attrs={"class": "form-controls form-control", "placeholder": "Project title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-controls form-control",
                    "rows": 3,
                    "placeholder": "Project description",
                }
            ),
            "year": forms.NumberInput(
                attrs={"class": "form-controls form-control", "placeholder": "2025"}
            ),
            "display_order": forms.NumberInput(
                attrs={"class": "form-controls form-control", "value": 0}
            ),
            "is_visible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ProducerSkillForm(forms.ModelForm):

    class Meta:

        model = ProducerSkill

        fields = [
            "name",
            "rating",
            "display_order",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-controls form-control", "placeholder": "Skill"}
            ),
            "rating": forms.NumberInput(
                attrs={"class": "form-controls form-control", "min": 1, "max": 5}
            ),
            "display_order": forms.NumberInput(
                attrs={"class": "form-controls form-control", "value": 0}
            ),
        }

