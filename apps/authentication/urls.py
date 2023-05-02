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
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", views.users_view, name="users"),
    path("users/add/", views.add_user_view, name="add_user"),
    path("users/<int:user_id>/edit", views.edit_user_view, name="edit_user"),
    path("users/<int:user_id>/activate", views.activate_user_view, name="activate_user"),
    path("users/<int:user_id>/deactivate", views.deactivate_user_view, name="deactivate_user"),
    path('users/<int:user_id>/reinit_password', views.reinit_password_view, name="reinit_password"),
    path("profiles/", views.profiles_view, name="profiles"),
    path("profiles/add/", views.add_profile_view, name="add_profile"),
    path("profiles/<uuid:profile_id>/edit", views.edit_profile_view, name="edit_profile"),
    path("agencies/", views.agencies_view, name="agencies"),
    path("agencies/add/", views.add_agency_view, name="add_agency"),
    path("agencies/<int:agency_id>/edit", views.edit_agency_view, name="edit_agency"),
    path("permissions/", views.permissions_view, name="permissions"),
    path("permissions/add/", views.add_permission_view, name="add_permissions"),
    path("permissions/<int:permission_id>/edit", views.edit_permission_view, name="edit_permission"),
    path("permissions/<int:permission_id>/delete", views.delete_permission_view, name="delete_permission"),
]
