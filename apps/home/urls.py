# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.urls import path, re_path
from apps.home import views

app_name = 'home'

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path("graphs/", views.graphs_view, name='graphs'),
    path("users/<int:user_id>/profile", views.page_profile_view, name='page_profile'),
    path("users/<int:user_id>/profile/edit", views.edit_page_profile_view, name='page_profile_edit'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
