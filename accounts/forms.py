from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Role")

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
