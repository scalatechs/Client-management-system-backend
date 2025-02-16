from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.accounts.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

class SignInForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)
