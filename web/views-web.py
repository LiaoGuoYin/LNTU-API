# urlpatterns = [
#     url(r'', include(route.urls))
#     # path('home/', views.home, name="home"),
#     # path('', views.login, name="login"),
#     # path('cet/', views.getCET, name="cet"),
#     # path('scores/', views.getScores, name="scores"),
# ]
#

# from django.http import HttpResponse
# from django.shortcuts import render
#
# from spider.client import Client
# from web.models import CET, Score
# from web.serializers import ScoreSerializer
#
#
# def home(request):
#     scores = Score.objects.filter(name="管理统计学")
#     scores_serializer = ScoreSerializer(scores, many=True)
#     return HttpResponse(scores_serializer.data)
#
#
# def login(request):
#     if request.method == "POST":
#         username = request.GET['username']
#         password = request.GET['password']
#         try:
#             client = Client(username, password)
#             client.getStudentInfo()
#             client.getScores()
#             context = "success"
#         except Exception as e:
#             context = "username or password error or Office online down"
#         return render(request, 'login.html', {'context': context})
#     else:
#         return render(request, 'login.html', {'context': "hold on logging"})
#         # return HttpResponse("GET method is not support..")
#
#
# def getScores(request):
#     if request.method == 'GET':
#         username = request.GET.get('username')
#         scores = Score.objects.filter(username=username)
#         name_and_verbose = {each.name: each.verbose_name for each in Score._meta.get_fields()}
#         context = {'scores': scores, 'name_and_verbose': name_and_verbose}
#         return render(request, 'scores.html', {'context': context})
#     else:
#         return HttpResponse("POST method is not support..")
#
#
# def getCET(request):
#     if request.method == "GET":
#         username = request.GET['username']
#         scores = CET.objects.filter(username=username)
#         name_and_verbose = {each.name: each.verbose_name for each in CET._meta.get_fields()}
#         name_and_verbose.pop('id')
#         context = {'scores': scores, 'name_and_verbose': name_and_verbose}
#         return render(request, 'cet.html', {'context': context})
#     else:
#         return HttpResponse("POST method is not support..")
