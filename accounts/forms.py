from django import forms
from django.core.validators import RegexValidator
from allauth.account.forms import SignupForm as AllauthSignupForm

from .utils import phone_number_regex, postal_code_regex
from .models import User


class SignupForm(AllauthSignupForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(
            max_length=10,
            validators=[
                RegexValidator(
                    regex=phone_number_regex,
                    message="Example: 5141234567")
            ],
    )
    postal_code = forms.CharField(
            max_length=6,
            validators=[
                RegexValidator(
                    regex=postal_code_regex,
                    message="Example: H3L3L3")
            ],
    )
    members_per_account = forms.IntegerField(min_value=1, max_value=20)


class UserUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=phone_number_regex,  # Adjust regex as needed
                message="Phone number must be 10 digits."
            )
        ],
        required=False,
    )
    postal_code = forms.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex=postal_code_regex,  # Example: H3L3L3
                message="Postal code must be in the format: H3L3L3."
            )
        ],
        required=False,
    )
    members_per_account = forms.IntegerField(min_value=1, max_value=20)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'postal_code', 'members_per_account']
