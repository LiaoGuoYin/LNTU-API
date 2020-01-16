from django.http import HttpResponse
from django.shortcuts import render

from Spider.Capture.Client import Client


def getCET(request):
    if request.method == 'GET':
        userId = request.GET.get('username')
        password = request.GET.get('password')
        client = Client(userId, password)
        result_lists = client.getCET()
        return render(request, 'login.html', {"CETS": result_lists})
    else:
        return HttpResponse("The POST method is not support")


def getScores(request):
    if request.method == 'GET':
        userId = request.GET.get('username')
        password = request.GET.get('password')
        client = Client(userId, password)
        result_dicts = client.getScores()
        print(result_dicts)
        return render(request, 'scores.html', {"scores": result_dicts})
    else:
        return HttpResponse("The POST method is not support")


def login(request):
    if request.method == "POST":
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        # client = Client(username, password)
        # client.getScores()
        return HttpResponse("Processing..")
    else:
        return HttpResponse("GET method is coding..")
