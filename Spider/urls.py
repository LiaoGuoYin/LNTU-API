from django.urls import path

from Spider import views

urlpatterns = [
    path('', views.login, name="login"),
    path('cet/', views.getCET, name="cet"),
    path('scores/', views.getScores, name="scores"),
]
