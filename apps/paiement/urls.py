# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.urls import path, re_path
from apps.paiement import views

app_name = 'paiement'

urlpatterns = [

    # The home page
    path('', views.index, name='index'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
