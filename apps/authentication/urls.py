# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('reset_password/', views.reset_password_view, name="reset_password"),
    path('register/', views.register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", views.users_view, name="users"),
    path("profiles/", views.profiles_view, name="profiles"),
    path("profiles/add/", views.add_profile_view, name="add_profile")
]
