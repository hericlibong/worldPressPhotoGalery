from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta :
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label ='User')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label ='Password')

