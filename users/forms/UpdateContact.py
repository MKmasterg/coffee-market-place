from django import forms
from django.core import validators

class UpdateUserForm(forms.Form):
    phone_number = forms.CharField(
        label="Phone number",
        validators=[validators.MaxLengthValidator(11,"Phone number must be 11 characters"),
                    validators.MinLengthValidator(11,"Phone number must be 11 characters")
        ],
    help_text="09xxxxxxxxx or 021xxxxxxxx",
    required=True
    )
    home_address = forms.CharField(
        label="Home address",
        help_text="If you are a seller then you can leave this field empty",
        required=False
    )