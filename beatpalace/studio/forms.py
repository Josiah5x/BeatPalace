from django.utils import timezone
from django.core.exceptions import ValidationError

from django import forms
from .models import StudioService

from .models import (
    Studio,
     StudioImage,
     Workspace,
     StudioService,
     StudioBooking,
)

class StudioForm(forms.ModelForm):

    class Meta:
        model = Studio

        fields = [
            "name",
            "studio_type",
            "description",
            "address",
            "city",
            "state",
            "country",
            "phone",
            "email",
            "hourly_rate",
            "daily_rate",
            "capacity",
            "equipment",
            "amenities",
            "rules",
            "cover_image",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. BeatPalace Recording Studio",
                }
            ),

            "studio_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe your studio...",
                }
            ),

            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Studio address",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "City",
                }
            ),

            "state": forms.Select(
                attrs={
                    "class": "form-select",
                    "placeholder": "State",
                }
            ),
            
            # forms.TextInput(
            #     attrs={
            #         "class": "form-control",
            #         "placeholder": "State",
            #     }
            # ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Contact phone",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "studio@example.com",
                }
            ),

            "hourly_rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                    "placeholder": "0.00",
                }
            ),

            "daily_rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                    "placeholder": "Optional",
                }
            ),

            "capacity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                }
            ),

            "equipment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Microphones, speakers, MIDI keyboard, instruments...",
                }
            ),

            "amenities": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Air conditioning, Wi-Fi, parking...",
                }
            ),

            "rules": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Studio rules...",
                }
            ),

            "cover_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


class WorkspaceForm(forms.ModelForm):

    class Meta:
        model = Workspace

        fields = [
            "name",
            "description",
            "hourly_rate",
            "capacity",
            "equipment",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Main Recording Room",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe this workspace...",
                }
            ),

            "hourly_rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                    "placeholder": "15000",
                }
            ),

            "capacity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                }
            ),

            "equipment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Microphones, monitors, keyboard, instruments...",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }



class StudioBookingForm(forms.ModelForm):

    services = forms.ModelMultipleChoiceField(
        queryset=StudioService.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:

        model = StudioBooking

        fields = [
            "workspace",
            "booking_date",
            "start_time",
            "end_time",
            "number_of_people",
            "notes",
        ]

        widgets = {

            "workspace": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "booking_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "start_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "end_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "number_of_people": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": (
                        "Tell the studio anything "
                        "they should know..."
                    ),
                }
            ),
        }

    def __init__(self, *args, studio=None, **kwargs):

        super().__init__(*args, **kwargs)

        self.studio = studio

        if studio:

            self.fields[
                "workspace"
            ].queryset = studio.workspaces.filter(
                is_active=True
            )

            self.fields[
                "services"
            ].queryset = studio.services.filter(
                is_active=True
            )

    def clean(self):

        cleaned_data = super().clean()

        booking_date = cleaned_data.get(
            "booking_date"
        )

        start_time = cleaned_data.get(
            "start_time"
        )

        end_time = cleaned_data.get(
            "end_time"
        )

        workspace = cleaned_data.get(
            "workspace"
        )

        number_of_people = cleaned_data.get(
            "number_of_people"
        )

        if not all([
            booking_date,
            start_time,
            end_time,
        ]):
            return cleaned_data

        if start_time >= end_time:

            raise ValidationError(
                "End time must be later than start time."
            )

        if booking_date < timezone.localdate():

            raise forms.ValidationError(
                "You cannot book a date in the past."
            )

        if workspace:

            if number_of_people > workspace.capacity:

                raise ValidationError(
                    f"This workspace can only accommodate "
                    f"{workspace.capacity} people."
                )

            booking_exists = StudioBooking.objects.filter(
                workspace=workspace,
                booking_date=booking_date,
                status__in=[
                    "pending",
                    "confirmed",
                    "in_session",
                ],
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exists()

            if booking_exists:

                raise ValidationError(
                    "This workspace is already booked "
                    "during the selected time."
                )

        return cleaned_data




class StudioServiceForm(forms.ModelForm):

    class Meta:
        model = StudioService

        fields = [
            "name",
            "description",
            "price",
            "price_type",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Mixing & Mastering",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe this service...",
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0.00",
                    "step": "0.01",
                }
            ),

            "price_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }