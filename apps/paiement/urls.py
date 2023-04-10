# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.urls import path, re_path
from apps.paiement import views, printviews

app_name = 'paiement'

urlpatterns = [

    path("payments/", views.payments_view, name="payments"),
    path("payments/add/", views.add_payment_view, name="add_payment"),
    path("payments/generate/", views.generate_payment_view, name="generate_payment"),
    path("payments/<int:payment_id>/edit", views.edit_payment_view, name="edit_payment"),
    path("payments/<int:payment_id>/print", printviews.payment_receipt_view, name="payment_receipt"),
    path("declarations/", views.declarations_view, name="declarations"),
    path("declarations/add/", views.add_declaration_view, name="add_declaration"),
    path("declarations/<int:declaration_id>/edit", views.edit_declaration_view, name="edit_declaration"),
    path("declarations/<int:declaration_id>/validate", views.validate_declaration_view, name="validate_declaration"),
    path("declarations/<int:declaration_id>/bill", views.bill_declaration_view, name="bill_declaration"),
    path("declarations/<int:declaration_id>/print", printviews.declaration_receipt_view, name="declaration_receipt"),
    path("factures/", views.factures_view, name="factures"),
    path("factures/add/", views.add_facture_view, name="add_facture"),
    path("factures/<int:bill_id>/print", printviews.bill_receipt_view, name="bill_receipt"),
    path("devises/", views.devises_view, name="devises"),
    path("devises/update", views.devises_update_view, name="update_devises"),
    path("devises/<int:permit_id>/<int:devise_id>/value", views.get_devise_value, name="get_devise_value"),
    path("devises/<int:devise_id>/value", views.get_devise, name="get_devise"),
]
