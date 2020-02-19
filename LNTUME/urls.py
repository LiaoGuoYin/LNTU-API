"""LNTUME URL Configuration
"""
from django.urls import path, include

urlpatterns = [
    path('', include('web.urls')),
    path('api/v1/', include('api.urls')),
    # path('admin/', admin.site.urls),
    # path('aipao/', include('aipao.urls')),
    # path('spider/', include('spider.urls')),
]
