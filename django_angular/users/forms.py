from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from users.models import MpesaCode

PAYMENT_CHOICES = (
    ('M', 'MPESA'),
    #('P', 'PayPal')
)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.IntegerField()

    class Meta:
        model = User
        fields = [
            'username', 'email', 'phone', 'password1', 'password2'
        ]

class CheckoutForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    mobi_number = forms.IntegerField(required=True)
    delivery_address = forms.CharField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class MpesaCodeForm(forms.ModelForm):
    code = forms.CharField(min_length=10)
    class Meta:
        model = MpesaCode
        fields = ['code',]
    