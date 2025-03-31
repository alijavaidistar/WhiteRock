'''
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Role")

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

'''



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Removed 'role'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "basic"  # Set default role to 'basic'
        if commit:
            user.save()
        return user
