# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.contrib import admin
from django.urls import path, include  # add this

from django.conf import settings
from django.conf.urls.static import static

from apps.paiement import apiviews

# import routers
from rest_framework import routers

# define the router
# router = routers.DefaultRouter()
#router = routers.SimpleRouter()

# define the router path and viewset to be used
#router.register(r'tdss-api/get-declarations', apiviews.DeclarationViewSet)
def home(request):
    return HttpResponse("Hello, Django is running!")

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.paiement.urls")),
    path("", include("apps.home.urls")),             # UI Kits Html files
   # path("api-auth/", include('rest_framework.urls')), # For API calls
] + router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
