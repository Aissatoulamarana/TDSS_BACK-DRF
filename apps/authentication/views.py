# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm, ProfileForm, CustomUserForm, ResetPwdForm
from .models import CustomUser, ProfileType, Profile, Region, Agency
import secrets, string
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib import messages
from django.forms import ValidationError

# Create your views here.

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.reset_pwd == True:
                    return redirect("authentication:reset_password")
                else:
                    return redirect("/")
            else:
                msg = 'Email/Mot de passe incorrect.'
        else:
            msg = 'Formulaire invalid soumit.'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def reset_password_view(request):
    msg = None
    form = ResetPwdForm(request.POST or None)

    if request.method == "POST":
        
        if form.is_valid():
            oldpwd = form.cleaned_data.get("old_password")
            newpwd = form.cleaned_data.get("new_password")
            confpwd = form.cleaned_data.get("confirmation_pwd")
            if newpwd != confpwd:
                msg = "Les mots de passe sont différents."
                
            else:
                user = authenticate(username=request.user.username, password=oldpwd)
                if user is not None:
                    user.set_password(newpwd)
                    user.reset_pwd = False
                    user.save()
                    return redirect("/")
                else:
                    msg = "Ancien mot de passe incorrect."

        else:
            msg = "Formulaire invalid soumit."
    
    return render(request, "accounts/reset-password.html", {"form": form, "msg": msg})


def users_view(request):
    users = CustomUser.objects.all()

    return render(request, "accounts/users.html", {
        'users': users,
        'segment': "administration"
    })


def profiles_view(request):
    profiles = Profile.objects.all()
    form = ProfileForm()
    userform = CustomUserForm()

    return render(request, "accounts/profiles.html", {
        #  To edit
        'form': form,
        'userform': userform,
        'profiles': profiles,
        'segment': "administration"
    })


def add_profile_view(request):
    default_region = Region.objects.first()
    initial_value = {'location': default_region}
    context_empty = {
        'profileform': ProfileForm(prefix= "profile", initial= initial_value), 
        'userform': CustomUserForm(prefix= "user"), 
        'segment': 'administration'
    }

    if request.method == "POST":

        profileform = ProfileForm(request.POST, request.FILES, prefix= "profile")
        userform = CustomUserForm(request.POST, prefix= "user")
        
        if profileform.is_valid() and userform.is_valid():
            print("Valid forms submitted!")

            new_user = userform.save(commit=False)
            random_pwd = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(8)))
            new_user.username = new_user.email
            new_user.set_password(random_pwd)
            new_user.created_by = request.user

            new_user.save()
            print("User created!")

            send_mail(
                "Creation de nouveau compte",
                f"Bonjour, un compe a été créer pour vous sur le site de paiement. MDP: {random_pwd}",
                "noreply.odiallo@gmail.com",
                [new_user.email],
                fail_silently=False
            )
            print("Mail sent!")

            new_profile = profileform.save(commit=False)
            new_profile.account = new_user
            new_profile.created_by = request.user

            new_profile.save()
            print("Profile created!")

            messages.success(request, "Nouveau profil ajouté. <br> Un compte utilisateur a été crée pour le responsable.")
            return redirect("authentication:profiles")
        else:
            context = {
                'profileform': profileform, 
                'userform': userform, 
                'ErrorMessage': "Formulaire invalid soumit",
                'segment': 'administration'
            }
            return render(request, "accounts/add-profile.html", context)
        
    return render(request, "accounts/add-profile.html", context_empty)


def add_user_view(request):
    default_region = Region.objects.first()
    default_agency = Agency.objects.first()
    initial_value = {'location': default_region, 'agency': default_agency}
    context_empty = {'userform': CustomUserForm(initial= initial_value), 'segment': 'administration'}
    
    if request.method == "POST":
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            random_pwd = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(8)))
            new_user = form.save(commit=False)
            new_user.username = new_user.email
            new_user.set_password(random_pwd)
            new_user.created_by = request.user
            # print(random_pwd)

            new_user.save()
            print("user created!")

            send_mail(
                "Creation de nouveau compte",
                f"Bonjour, un compe a été créer pour vous sur le site de paiement. MDP: {random_pwd}",
                "noreply.odiallo@gmail.com",
                [new_user.email],
                fail_silently=False
            )
            print("mail sent!")
            
            messages.success(request, "Nouveau compte utilisateur ajouté. <br> Une notification a été envoyé par mail.")
            return redirect("authentication:users")
        else:
            context = {'userform': form, 'ErrorMessage': "Formulaire invalid soumit.", 'segment': 'administration'}
            return render(request, "accounts/add-user.html", context)

    return render(request, "accounts/add-user.html", context_empty)


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
