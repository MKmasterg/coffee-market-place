from django import forms
from django.core import validators


class Selector(forms.Form):
    ROLES=[
        (1,"Customer"),
        (2,"Seller")
    ]
    helpT = "If you want to buy select customer\nIf you want to sell select seller"
    role_selector = forms.IntegerField(
        help_text=helpT,
        validators=[
            validators.MinValueValidator(1,"Invalid input!"),
            validators.MaxValueValidator(2,"Invalid input!")
        ],
        label="Role",
        widget=forms.Select(choices=ROLES),
        required=True
    )

class RoleCustomer(forms.Form):
    home_address = forms.CharField(
        label="Home address",
        help_text="Please insert your address for delivery",
        required=True
    )

class MarketForm(forms.Form):
    name = forms.CharField(
        label="Market's name",
        validators=[
            validators.MinLengthValidator(3,"Market's name must be at least 3 of length!")
        ],
        required=True
    )
    desc = forms.CharField(label="Description",required=True)
    address = forms.CharField(label="Address",required=True)
    phone_number = forms.CharField(
        label="Phone number" ,
        help_text="09xxxxxxxxx or 021xxxxxxxx",
        validators=[
            validators.MinLengthValidator(11,"The phone number must be 11 digits"),
            validators.MaxLengthValidator(11,"The phone number must be 11 digits")
        ],
        required=True
    )
    is_active = forms.BooleanField(required=False)

class SellerAssignmentForm(forms.Form):
    seller_username = forms.CharField(
        label="Seller's username",
        help_text="Please enter the seller's username",
        required=True
    )