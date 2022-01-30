from django import forms
from django.forms import PasswordInput, TextInput
from .models import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth import password_validation


class CustomUserForm(UserCreationForm):
    """This form allows our custom user model to be registered with an added field reflecting its employee status"""
    is_employee = forms.BooleanField(label="Check to register as employee", required=False)
    password1 = forms.CharField(
        label= ("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': "form-control mb-1 mt-1",}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label= ("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': "form-control mb-1 mt-1",}),
        strip=False,
        help_text= ("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "is_employee")
        field_classes = {'username': UsernameField, 'password1': PasswordInput}

        widgets = {
            'username': TextInput(attrs={
                'class': "form-control mb-1 mt-1",
                'placeholder': 'Username',
                }),
            'password1': PasswordInput(attrs={
                'autocomplete': 'new-password',
                'class': "form-control mb-1, mt-1",
                'placeholder': 'Password'
            })
        }
        
    def save(self, commit=True):
        # Overriding the save method to add user to auth group of Employee or Customer depending on if box is checked
        user = super(CustomUserForm, self).save(commit=False)
        user.is_employee = self.cleaned_data["is_employee"]

        # If you get an exception here, you need to create the Employee/Customer groups in the Admin interface
        if commit:
            user.save()
            if user.is_employee:
                employees = Group.objects.get(name="Employees")
                employees.user_set.add(user)
            else:
                customers = Group.objects.get(name="Customers")
                customers.user_set.add(user)
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': "form-control mb-1 mt-1", 'placeholder': 'Username',}))
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'placeholder': 'Password', 'class': "form-control mb-3 mt-1"}),
    )

