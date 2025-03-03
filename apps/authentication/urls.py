# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.urls import path, include
from .views import (
    AgencyDetailView, 
    AgencyListView, 
    add_agency_view,
    
    PermissionDetailView, 
    PermissionListView, 
    add_permission_view,
    
    ProfileDetailView, 
    ProfileListView, 
    add_profile_api,
    
    DeactivateUserView, 
    LogoutView
)



app_name = 'authentication'

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),  # JWT Token endpoints
    path("auth/jwt/logout/", LogoutView.as_view(), name="jwt-logout"),
    path('api/deactivate_user/<int:user_id>/', DeactivateUserView.as_view(), name='deactivate_user'),

    path('add-permission/', add_permission_view, name='add_permission'),
    path('api/permissions/', PermissionListView.as_view(), name='permission_list'),
    path('api/permissions/<int:permission_id>/', PermissionDetailView.as_view(), name='permission_detail'),

    path('add-agency/', add_agency_view, name='add_agency'),
    path('api/agencies/', AgencyListView.as_view(), name='agency_list'),
    path('api/agencies/<int:agency_id>/', AgencyDetailView.as_view(), name='agency_detail'),

    path('add-profile/', add_profile_api, name='add_profile_api'),
    path('api/profiles/', ProfileListView.as_view(), name='profile_list'),
    path('api/profiles/<int:profile_id>/', ProfileDetailView.as_view(), name='profile_detail'),
]
