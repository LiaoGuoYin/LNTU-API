# from rest_framework import viewsets
#
# from web.models import User
# from web.serializers import UserSerializer
#
#
# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
from django.http import Http404
from django.shortcuts import render, redirect
from rest_framework.views import APIView

from web.forms import LoginForm


class UserView(APIView):
    def get(self, request, format=None):
        # user = User.objects.all()
        # serializer = UserSerializer(user, many=True)
        # return Response(serializer.data)
        return render(request, template_name='user.html', context=context)

    def post(self, request, format=None):
        pass


def login(request):
    if request.method == "POST":
        print("POST method")
        form = LoginForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            print(form.__dict__)
            return redirect(login)
    elif request.method == "GET":
        print("GET method")
        form = LoginForm()
    else:
        print("unknown method")
        return Http404
    print(locals())
    return render(request, 'login.html', locals())

#
# def contact(request):
#     if request.method == "POST":
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             cd = form.clean_message()
#             print(cd)
#             return redirect('login')
#         else:
#             form = ContactForm()
#             form.message = "error"
#     return render(request, 'contract.html', locals())
#
#
# def search(request):
#     q = request.GET.get('q')
#     error_message = ''
#     if not q:
#         error_message = 'Input a keyword please'
#         return render(request, 'login.html', locals())
