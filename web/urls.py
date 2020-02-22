from django.urls import path

from web import views
from web.views import UserView

urlpatterns = [
    path('', views.login, name='login'),
    path('user/', UserView.as_view(), name='user'),
]
