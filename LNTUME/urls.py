"""LNTUME URL Configuration
"""
from django.urls import path, include

urlpatterns = [
    path('', include('api.urls')),
    # path('', include('web.urls')),
    # path('admin/', admin.site.urls),
    # path('aipao/', include('aipao.urls')),
    # path('spider/', include('spider.urls')),
]
