"""LNTUME URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('web.urls')),
    path('aipao/', include('aipao.urls'))
]
