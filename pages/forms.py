from django.contrib.auth.models import User
from django import forms
from registration.forms import RegistrationFormUniqueEmail


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']



