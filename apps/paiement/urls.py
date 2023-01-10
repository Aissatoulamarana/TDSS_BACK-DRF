# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.urls import path, re_path
from apps.paiement import views

app_name = 'paiement'

urlpatterns = [

    path("payments/", views.payments_view, name="payments"),
    path("devises/", views.devises_view, name="devises"),

]
