# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.urls import path
from .views import login_view, register_user, users_view, profiles_view, add_profile_view
from django.contrib.auth.views import LogoutView

app_name = 'authentication'

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", users_view, name="users"),
    path("profiles/", profiles_view, name="profiles"),
    path("profiles/add/", add_profile_view, name="add_profile")
]
