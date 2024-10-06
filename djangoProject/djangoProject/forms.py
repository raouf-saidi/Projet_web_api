from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'address', 'phone_number', 'password1']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        }
        help_texts = {
            'username': None,  # Disable help text
            'password1': None,  # Disable help text
            'password2': None,  # Disable help text

        }
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))