from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'first_name', 'last_name', 'phone', 'address' ]
        widgets = {
            'image': forms.FileInput(),
            'first_name' : forms.TextInput(attrs={'placeholder': 'Ingresa tu nombre'}),
            'last_name' : forms.TextInput(attrs={'placeholder': 'Ingresa tu apellido'}),
            'phone' : forms.Textarea(attrs={'rows':3, 'placeholder': 'Tu numero'}),
            'address' : forms.TextInput(attrs={'placeholder': 'Tu direccion'}),
        }
        
        
class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']
