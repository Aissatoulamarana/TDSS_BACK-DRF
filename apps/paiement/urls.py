# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.urls import path, include
from apps.paiement import views, printviews, apiviews, exportviews 


from rest_framework.urlpatterns import format_suffix_patterns

app_name = "paiement"

urlpatterns = [
   
    path("payments/add/", views.add_payment_view, name="add_payment"),
   
    path(
        "payments/<int:payment_id>/print",
        printviews.payment_receipt_view,
        name="payment_receipt",
    ),
  
    path(
        "declarations/<int:declaration_id>/employee-renew",
        views.declaration_employee_renew,
        name="employee-renew",
    ),
   
    path(
        "declarations/<int:declaration_id>/print",
        printviews.declaration_receipt_view,
        name="declaration_receipt",
    ),
    
    path("factures/add/", views.add_facture_view, name="add_facture"),
    path(
        "factures/<int:bill_id>/print",
        printviews.bill_receipt_view,
        name="bill_receipt",
    ),
    path("devises/", views.devises_view, name="devises"),
    path("devises/update", views.devises_update_view, name="update_devises"),
    path(
        "devises/<int:permit_id>/<int:devise_id>/value",
        views.get_devise_value,
        name="get_devise_value",
    ),
    path("devises/<int:devise_id>/value", views.get_devise, name="get_devise"),
    path("agenges/print", exportviews.exportpdf_agencies_view, name="print_agencies"),
    path("profils/print", exportviews.exportpdf_profiles_view, name="print_profiles"),
    path("users/print", exportviews.exportpdf_users_view, name="print_users"),
    path(
        "permissions/print",
        exportviews.exportpdf_permissions_view,
        name="print_permissions",
    ),
    path("devises/print", exportviews.exportpdf_devises_view, name="print_devises"),
    path("payments/print", exportviews.exportpdf_payments_view, name="print_paiements"),
    path("bills/print", exportviews.exportpdf_bills_view, name="print_bills"),
    path(
        "declarations/print",
        exportviews.exportpdf_declarations_view,
        name="print_declarations",
    ),
    path(
        "agenges/export", exportviews.exportxlsx_agencies_view, name="export_agencies"
    ),
    path(
        "profils/export", exportviews.exportxlsx_profiles_view, name="export_profiles"
    ),
    path("users/export", exportviews.exportxlsx_users_view, name="export_users"),
    path(
        "permissions/export",
        exportviews.exportxlsx_permissions_view,
        name="export_permissions",
    ),
    path("devises/export", exportviews.exportxlsx_devises_view, name="export_devises"),
    path(
        "payments/export", exportviews.exportxlsx_payments_view, name="export_paiements"
    ),
    path("bills/export", exportviews.exportxlsx_bills_view, name="export_bills"),
    path(
        "declarations/export",
        exportviews.exportxlsx_declarations_view,
        name="export_declarations",
    ),
    path("tdss-api/get-employees/", apiviews.employee_list, name="api_employees"),
    path(
        "tdss-api/get-employees/<str:pid>/",
        apiviews.employee_detail,
        name="api_employee_detail",
    ),
    path("tdss-api/get-payments/", apiviews.payment_list, name="api_payments"),

    path('api/job-categories/', views.job_category_list, name='job-category-list'),
    path("jobs/", views.job_list, name="job-list"),  # GET et POST
    path('api_dec/', views.declaration_list, name='declaration-list'),
    path('create_dec/', views.declaration_create, name='declaration-create'),
    path('api/check-passport/', views.check_passport, name='check-passport'),
    path('details-declaration/<int:pk>/', views.declaration_detail, name='declaration-detail'),
    path('update-status/<int:pk>/', views.declaration_status_update, name='declaration-update-status'),
    path('facturer-dec/<int:declaration_id>/', views.facturer_declaration_api, name='bill-declaration-api'),
    path('api_factures/', views.factures_view_api, name='factures_api'),
    path('api/paid-facture/<int:facture_id>/', views.paid_facture, name='paid-facture-api'),
    path('api/payments/', views.list_paiements, name='api_payments'),
    path('api/jobs/<int:job_id>/', views.job_update, name='api_jobs'),
   
]

urlpatterns = format_suffix_patterns(urlpatterns)
