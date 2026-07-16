from django import forms
from django.core.validators import MaxLengthValidator


class StockRegistrationForm(forms.Form):
    name = forms.CharField(
        label="Name",
        validators=[MaxLengthValidator(40,"Name's max length is 40 characters"),],
        required=True
    )
    desc = forms.CharField(
        label="Description",
        validators=[MaxLengthValidator(100,"Description's max length is 100 characters"),],
        required=True
    )

    no = forms.IntegerField(
        label="Number of stock",
        required=True
    )
    is_available = forms.BooleanField(required=False)
    ppg = forms.CharField(
        label="Price per gram",
        help_text="Elaborating more might help in customers' decisions",
        validators=[MaxLengthValidator(50,"price description's max length is 50 characters"),],
        required=True
    )