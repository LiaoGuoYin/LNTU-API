from django.http import HttpResponse
from django.shortcuts import render

from Spider.Capture.Client import Client


def getCET(request):
    client = Client(1710030105, '****')
    result_lists = client.getCET()

    return render(request, 'login.html', {"CETS": result_lists})


def getScores(request):
    client = Client(1710030105, '****')
    result_dicts = client.getScores()
    print(result_dicts)
    return render(request, 'scores.html', {"scores": result_dicts})


def login(request):
    if request.method == "POST":
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        # client = Client(username, password)
        # client.getScores()
        return HttpResponse("Processing..")
    else:
        return HttpResponse("GET method is coding..")
