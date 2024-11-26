from django import forms

class PaymentForm(forms.Form):
    full_name = forms.CharField(max_length=100, label='Full Name')
    address = forms.CharField(max_length=255, label='Address')
    phone_number = forms.CharField(max_length=15, label='Phone Number')
    email = forms.EmailField(label='Email Address')
