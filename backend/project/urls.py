"""
 Copyright 2023 The Scorch Authors.

project URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from account.urls import router as account_router

# Assemble the full set of resources under the API from
# each of the apps
master_router = routers.DefaultRouter()
master_router.registry.extend(account_router.registry)

urlpatterns = [
    # path('api/auth/', include('django.contrib.auth.urls')),
    path(r'api/v1/', include(master_router.urls)),
    path(r'admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
