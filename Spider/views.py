from django.http import HttpResponse
from django.shortcuts import render

from Spider.core.Client import Client
from Spider.models import User


def getCET(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        client = Client(username, password)
        result_lists = client.getCET()
        return render(request, 'login.html', {"CETS": result_lists})
    else:
        return HttpResponse("The POST method is not support")


def getScores(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        user = User.objects.get(pk=username)
        return render(request, 'scores.html', {"scores": user.score.all()})
    else:
        return HttpResponse("The POST method is not support")


def login(request):
    if request.method == "POST":
        return HttpResponse("Processing..")
    else:
        return HttpResponse("GET method is coding..")
