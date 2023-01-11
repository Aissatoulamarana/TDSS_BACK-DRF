# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.urls import path, re_path
from apps.paiement import views

app_name = 'paiement'

urlpatterns = [

    path("payments/", views.payments_view, name="payments"),
    path("payments/add/", views.add_payment_view, name="add_payment"),
    path("devises/", views.devises_view, name="devises"),
    path("devises/update", views.devises_update_view, name="update_devises"),

]
