# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.urls import path
from apps.paiement import views, printviews, apiviews, exportviews

from rest_framework.urlpatterns import format_suffix_patterns

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
    path("declarations/<int:declaration_id>/submit", views.submit_declaration_view, name="submit_declaration"),
    path("declarations/<int:declaration_id>/reject", views.reject_declaration_view, name="reject_declaration"),
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

    path("agenges/print", exportviews.export_agencies_view, name="print_agencies"),
    path("profils/print", exportviews.export_profiles_view, name="print_profiles"),
    path("users/print", exportviews.export_users_view, name="print_users"),
    path("permissions/print", exportviews.export_permissions_view, name="print_permissions"),
    path("devises/print", exportviews.export_devises_view, name="print_devises"),
    path("payments/print", exportviews.export_payments_view, name="print_paiements"),
    path("bills/print", exportviews.export_bills_view, name="print_bills"),
    path("declarations/print", exportviews.export_declarations_view, name="print_declarations"),
    
    path('tdss-api/get-employees/', apiviews.employee_list, name="api_employees"),
    path('tdss-api/get-employees/<str:pid>/', apiviews.employee_detail, name="api_employee_detail"),
    path('tdss-api/get-payments/', apiviews.payment_list, name="api_payments"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
