"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# -- My adds
from django.conf import settings
from django.conf.urls.static import static

from apps.paiement import apiviews

# import routers
from rest_framework import routers

# define the router
# router = routers.DefaultRouter()
router = routers.SimpleRouter()

# define the router path and viewset to be used
router.register(r'tdss-api/get-declarations', apiviews.DeclarationViewSet)

urlpatterns = []

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


urlpatterns += [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.paiement.urls")),
    path("", include("apps.home.urls")),             # UI Kits Html files
    # path("api-auth/", include('rest_framework.urls')), # For API calls
    path('api/', include("paiement.api_urls")),
]
