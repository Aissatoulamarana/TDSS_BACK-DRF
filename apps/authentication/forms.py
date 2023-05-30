# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django import forms
from django.forms import TextInput, NumberInput, Select, Textarea, FileInput, DateTimeInput, DateInput, EmailInput, RadioSelect, TimeInput, ClearableFileInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, CustomUser, ProfileType, UserType, Agency, Region, Permission


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
        fields = ('name', 'type', 'description', 'location', 'contact', 'picture', 'adresse', 'email')
        # Omitted fields: uuid, created_on, modified_on, status
        widgets = {
            'name': TextInput(attrs={'class': "form-control", 'placeholder': "Nom du profil", 'autofocus': "True"}),
            'type': Select(attrs={'class': "form-control", 'placeholder': "Type du profil"}),
            'description': Textarea(attrs={'rows':3, 'placeholder': "Description du profil...", 'class': "form-control" }),
            'location': Select(attrs={'class': "form-control", 'placeholder': "Emplacement"}),
            'contact': NumberInput(attrs={'class': "form-control", 'placeholder': "N° de contact", 'type': "number", 'min': 0}),
            'picture': ClearableFileInput(attrs={'class': "form-control"}),
            'adresse': Textarea(attrs={'rows':3, 'placeholder': "Adresse, BP...", 'class': "form-control" }),
            'email': EmailInput(attrs={'class': "form-control", 'placeholder': "example@mail.com"}),
        }
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['type'].empty_label = "Sélectionner le type"
        self.fields['type'].queryset = ProfileType.objects.filter(status='ON').order_by('id')
        self.fields['location'].empty_label = "Sélectionner l'emplacement"
  


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'location', 'agency', 'type', 'job', 'picture', 'permissions')
        # Omitted fields: username, profile, created_by, created_on, modified_on
        widgets = {
            'first_name': TextInput(attrs={'class': "form-control", 'placeholder': "Prenoms"}),
            'last_name': TextInput(attrs={'class': "form-control", 'placeholder': "Nom"}),
            'email': EmailInput(attrs={'class': "form-control", 'placeholder': "example@mail.com"}),
            'phone': NumberInput(attrs={'class': "form-control", 'placeholder': "N° de téléphone", 'type': "number", 'min': 0}),
            'location': Select(attrs={'class': "form-control", 'placeholder': "Emplacement/Région"}),
            'agency': Select(attrs={'class': "form-control", 'placeholder': "Agence"}),
            'type': Select(attrs={'class': "form-control", 'placeholder': "Type d'utilisateur"}),
            'job': TextInput(attrs={'class': "form-control", 'placeholder': "Poste"}),
            'picture': ClearableFileInput(attrs={'class': "form-control"}),
            'permissions': Select(attrs={'class': "form-control", 'placeholder': "Permissions"})
        }
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields['agency'].empty_label = "Sélectionner l'agence"
        self.fields['agency'].required = False
        self.fields['location'].empty_label = "Sélectionner l'emplacement..."
        self.fields['permissions'].empty_label = "Sélectionner les permissions..."
        self.fields['type'].empty_label = "Sélectionner le type"
        self.fields['type'].queryset = UserType.objects.filter(status='ON').order_by('id')


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ('name', 'profile_type', 'codes', 'list')
        # Omitteed fields: id, status
        widgets = {
            'name': TextInput(attrs={'class': "form-control", 'placeholder': "Nom de la permission"}),
            'profile_type': Select(attrs={'class': "form-control", 'placeholder': "Type de profil"}),
            'codes': Textarea(attrs={'rows':4, 'placeholder': "Code des autorisations...", 'class': "form-control" }),
            'list': Textarea(attrs={'rows':4, 'placeholder': "Liste des autorisations...", 'class': "form-control", 'readonly': "readonly" }),
        }
    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        self.fields['profile_type'].empty_label = "Sélectionner le type de profil..."


class AgencyForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ('code', 'region', 'name', 'comment')
        # Omitteed fields: id
        widgets = {
            'code': TextInput(attrs={'class': "form-control", 'placeholder': "Code de l'agence", 'autofocus': True}),
            'region': Select(attrs={'class': "form-control", 'placeholder': "Région"}),
            'name': TextInput(attrs={'class': "form-control", 'placeholder': "Nom de l'agence"}),
            'comment': Textarea(attrs={'rows':3, 'placeholder': "Commentaire...", 'class': "form-control" }),
        }
    def __init__(self, *args, **kwargs):
        super(AgencyForm, self).__init__(*args, **kwargs)
        self.fields['region'].empty_label = "Sélectionner la région"


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
