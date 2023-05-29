# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.contrib import admin
from django.urls import path, include  # add this

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = []

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

urlpatterns += [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.paiement.urls")),
    path("", include("apps.home.urls")),             # UI Kits Html files
]
 
