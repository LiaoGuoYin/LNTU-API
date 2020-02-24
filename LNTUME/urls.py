"""LNTUME URL Configuration"""
from django.conf.urls import url
from django.urls import path, include
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='LNTUME API')

urlpatterns = [
    path('', include('api.urls')),
    url('^schema/$', schema_view),
    # path('', include('web.urls')),
    # path('admin/', admin.site.urls),
    # path('aipao/', include('aipao.urls')),
    # path('spider/', include('spider.urls')),
]
