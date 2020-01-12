from django.urls import path

from Spider import views

urlpatterns = [
    path('', views.login, name="login"),
    path('getCET/', views.getCET, name="CET"),
    path('getScores/', views.getScores, name="Scores"),
]
