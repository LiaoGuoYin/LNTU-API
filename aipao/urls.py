from django.urls import path

from aipao import views

urlpatterns = [
    path('run/', views.run, name='run'),
]
