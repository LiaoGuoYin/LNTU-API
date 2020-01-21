from django.http import HttpResponse
from django.shortcuts import render

from Spider.models import CET, Score
from core.Client import Client


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            client = Client(username, password)
            client.getStudentInfo()
            client.getScores()
            context = "success"
        except Exception as e:
            context = "username or password error or Office online down"
        return render(request, 'login.html', {'context': context})
    else:
        return HttpResponse("GET method is not support..")


def getScores(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        scores = Score.objects.filter(username=username)
        name_and_verbose = {each.name: each.verbose_name for each in Score._meta.get_fields()}
        context = {'scores': scores, 'name_and_verbose': name_and_verbose}
        return render(request, 'scores.html', {'context': context})
    else:
        return HttpResponse("POST method is not support..")


def getCET(request):
    if request.method == "GET":
        username = request.GET['username']
        scores = CET.objects.filter(username=username)
        name_and_verbose = {each.name: each.verbose_name for each in CET._meta.get_fields()}
        name_and_verbose.pop('id')
        context = {'scores': scores, 'name_and_verbose': name_and_verbose}
        return render(request, 'cet.html', {'context': context})
    else:
        return HttpResponse("POST method is not support..")
