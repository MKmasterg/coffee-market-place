from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django import forms

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        validators=[
            validators.MinLengthValidator(2,"The username length must be between 2 and 20"),
            validators.MaxLengthValidator(20,"The username length must be between 2 and 20")
        ],
        required=True
    )
    phone_number = forms.CharField(
        label="Phone number" ,
        help_text="09xxxxxxxxx",
        validators=[
            validators.MinLengthValidator(11,"The phone number must be 11 digits"),
            validators.MaxLengthValidator(11,"The phone number must be 11 digits")
        ],
        required=True
    )
    id_number = forms.CharField(
        label="Id number",
        validators=[
            validators.MinLengthValidator(10,"The id number must be 10 digits"),
            validators.MaxLengthValidator(10,"The id number must be 10 digits")
        ],
        required=True
    )
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
        widget=forms.Select(choices=ROLES)
    )
    class Meta:
        model = User
        fields = ["username","first_name","last_name" ,"password1", "password2", "email" ]

