# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm, ProfileForm, CustomUserForm, ResetPwdForm, AgencyForm
from .models import CustomUser, ProfileType, Profile, Region, Agency, UserType
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

        userform.fields["type"].required = False
        
        if profileform.is_valid() and userform.is_valid():
            print("Valid forms submitted!")

            new_user = userform.save(commit=False)
            random_pwd = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(8)))
            new_user.username = new_user.email
            new_user.set_password(random_pwd)
            new_user.created_by = request.user
            new_user.type = UserType.objects.first()

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


def edit_user_view(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    context_empty = {'userform': CustomUserForm(instance=user), 'user_id': user_id, 'segment': 'administration'}

    if request.method == "POST":
        
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            print("User updated!")

            messages.success(request, "Compte utilisateur modifié avec succès !")
            return redirect("authentication:users")

        else:
            context = {'userform': form, 'ErrorMessage': "Formulaire invalid soumit.", 'user_id': user_id, 'segment': 'administration'}
            return render(request, "accounts/edit-user.html", context)


    return render(request, "accounts/edit-user.html", context_empty)


def edit_profile_view(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    context_empty = {'profileform': ProfileForm(instance=profile), 'profile_id': profile_id, 'segment': 'administration'}

    if request.method == "POST":
        
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            print("Profile updated!")

            messages.success(request, "Profil modifié avec succès !")
            return redirect("authentication:profiles")

        else:
            context = {'userform': form, 'ErrorMessage': "Formulaire invalid soumit.", 'profile_id': profile_id, 'segment': 'administration'}
            return render(request, "accounts/edit-profile.html", context)


    return render(request, "accounts/edit-profile.html", context_empty)



def agencies_view(request):
    agencies = Agency.objects.all()
    form = AgencyForm()

    return render(request, "accounts/agencies.html", {
        
        'form': form,
        'agencies': agencies,
        'segment': "administration"
    })


def add_agency_view(request):
    default_region = Region.objects.first()
    initial_value = {'region': default_region}
    context_empty = {'form': AgencyForm(initial= initial_value), 'segment': 'administration'}

    if request.method == "POST":
        form = AgencyForm(request.POST)

        if form.is_valid():
            new_agency = form.save()
            messages.success(request, "Nouvelle agence ajoutée avec succès !")
            return redirect("authentication:agencies")
        else:
            context = {'form': form, 'ErrorMessage': "Formulaire invalid soumit.", 'segment': 'administration'}
            return render(request, "accounts/add-agency.html", context)

    return render(request, "accounts/add-agency.html", context_empty)


def edit_agency_view(request, agency_id):
    agency = Agency.objects.get(pk=agency_id)
    context_empty = {'form': AgencyForm(instance=agency), 'agency_id': agency_id, 'segment': 'administration'}

    if request.method == "POST":
        
        form = AgencyForm(request.POST, instance=agency)
        if form.is_valid():
            form.save()
            print("Agency updated!")

            messages.success(request, "Agence modifiée avec succès !")
            return redirect("authentication:agencies")

        else:
            context = {'form': form, 'ErrorMessage': "Formulaire invalid soumit.", 'agency_id': agency_id, 'segment': 'administration'}
            return render(request, "accounts/edit-agency.html", context)


    return render(request, "accounts/edit-agency.html", context_empty)



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
