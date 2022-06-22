from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput

class SingUpForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control1'})),
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control1'}))
    
class Meta:
    models = User
    fields = ['username', 'password', 'password2']
    widget = {'username': TextInput(attrs={'class': 'form-control1'})}
