# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm, ProfileForm, CustomUserForm
from .models import CustomUser, ProfileType, Profile
import secrets, string
from django.db import IntegrityError
from django.core.mail import send_mail

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
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def users_view(request):
    users = CustomUser.objects.all()

    return render(request, "accounts/users.html", {
        'users': users,
        'segment': 'administration'
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
    context_empty = {'profileform': ProfileForm(), 'userform': CustomUserForm(), 'segment': 'administration'}

    if request.method == "POST":
        # user_form = CustomUserForm(post_data['first_name'], post_data['last_name'], post_data['email'], 
        #                             post_data['phone'], post_data['job'])
        first = request.POST["first_name"]
        last = request.POST["last_name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        job = request.POST["job"]
        random_pwd = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(8)))
        # Attemp to create a new user for the profile
        try:
            new_user = CustomUser.objects.create_user(email, email, random_pwd, first_name=first, last_name=last, phone=phone, job=job)
            new_user.save()

            send_mail(
                "Creation de nouveau compte",
                f"Bonjour, un compe a été créer pour vous sur le site de paiement. MDP: {random_pwd}",
                "noreply.odiallo@gmail.com",
                ["omatest80@gmail.com"],
                fail_silently=False
            )
        except IntegrityError:
            context = context_empty
            context['ErrorMessage'] = "Cet email existe déjà. "
            return render(request, "accounts/add-profile.html", context)
        
        # profileform = ProfileForm(request.POST, request.FILES)
        name = request.POST["name"]
        type = ProfileType.objects.get(pk=request.POST["type"])
        descrip = request.POST["description"]
        location = request.POST["location"]
        contact = request.POST["contact"]
        picture = request.FILES["picture"]

        new_profile = Profile(name=name, type=type, description=descrip, location=location, contact=contact, picture=picture)
        new_profile.account = new_user
        new_profile.created_by = request.user
        new_profile.save()

        print("Form submitted successfully!")
        

        

    return render(request, "accounts/add-profile.html", context_empty)


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
