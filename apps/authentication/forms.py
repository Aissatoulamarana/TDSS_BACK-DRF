# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django import forms
from django.forms import TextInput, NumberInput, Select, Textarea, FileInput, DateTimeInput, DateInput, EmailInput, RadioSelect, TimeInput, ClearableFileInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class ResetPwdForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control",
        'placeholder': "Ancien"
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control",
        'placeholder': "Nouveau"
    }))
    confirmation_pwd = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control",
        'placeholder': "Confirmation"
    }))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'type', 'description', 'location', 'contact', 'status', 'picture')
        # Omitted fields: uuid, account, created_by, created_on, modified_on
        widgets = {
            'name': TextInput(attrs={'class': "form-control", 'placeholder': "Nom du profil", 'autofocus': "True"}),
            'type': Select(attrs={'class': "form-control", 'placeholder': "Type du profil"}),
            'description': Textarea(attrs={'rows':3, 'placeholder': "Description du profil...", 'class': "form-control" }),
            'location': Select(attrs={'class': "form-control", 'placeholder': "Emplacement"}),
            'contact': NumberInput(attrs={'class': "form-control", 'placeholder': "N° de contact", 'type': "number", 'min': 0}),
            'picture': ClearableFileInput(attrs={'class': "form-control"})
        }


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'location', 'agency', 'job', 'picture')
        # Omitted fields: username, created_by, created_on, modified_on
        widgets = {
            'first_name': TextInput(attrs={'class': "form-control", 'placeholder': "Prenoms"}),
            'last_name': TextInput(attrs={'class': "form-control", 'placeholder': "Nom"}),
            'email': EmailInput(attrs={'class': "form-control", 'placeholder': "example@mail.com"}),
            'phone': NumberInput(attrs={'class': "form-control", 'placeholder': "N° de téléphone", 'type': "number", 'min': 0}),
            'location': Select(attrs={'class': "form-control", 'placeholder': "Emplacement/Région"}),
            'agency': Select(attrs={'class': "form-control", 'placeholder': "Agence"}),
            'job': TextInput(attrs={'class': "form-control", 'placeholder': "Poste"}),
            'picture': FileInput(attrs={'class': "form-control"})
        }


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
