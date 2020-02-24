from rest_framework import exceptions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth import Authentication, md5
from api.models import User, UserToken, ClassRoom
from api.serializers import StudentInfoModelSerializer, \
    CETModelSerializer, ScoreModelSerializer, ExamPlanModelSerializer, CoursePlanModelSerializer, \
    ClassRoomModelSerializer, UserModelSerializer
from spider.client import Client


class AuthView(APIView):
    """Login and Authorization return token"""

    def post(self, request, *args, **kwargs):
        ret = {
            'status': False,
            'msg': '登陆失败，请检查用户名或密码',
        }
        try:
            username = request.POST.get('username').split()[0]
            password = request.POST.get('password').split()[0]
            client = Client(username=username, password=password)
            user_obj = User.objects.update_or_create(username=username, password=password)[0]
            token = md5(username)
            UserToken.objects.update_or_create(user=user_obj, defaults={'token': token})
            ret = {
                'status': True,
                'msg': 'login success',
                'token': token,
            }
        except AttributeError:
            ret['msg'] = "用户名或密码为空!"
        except AuthenticationFailed as e:
            ret['msg'] = str(e)
        return Response(ret)

    def get(self, request):
        return Response({
            'status': False,
            'msg': 'Invalid HTTP Method',
        })


class BaseView(APIView):
    """自定义的通用基类，实现get获取，post,patch更新"""
    authentication_classes = [Authentication, ]
    serializer_class = None
    model_related_name = None
    client = None
    client_method = None

    def get_user_obj(self):
        """With HTTPHeaders 'authorization' filed's token to query related user model"""
        return self.request.user.user

    def login(self):
        user_obj = self.get_user_obj()
        try:
            self.client = Client(username=user_obj.username, password=user_obj.password)
        except:
            raise exceptions.APIException("username or password error!")

    def get(self, request):
        """Serialize related_query_instance, and return JSON"""
        """序列化反向查询结果，并返回 JSON"""
        assert self.serializer_class is not None, ("Must override the serializer_class")
        assert self.model_related_name is not None, ("Must override the model_related_name")

        user_obj = self.get_user_obj()
        query_related_obj = getattr(user_obj, self.model_related_name)
        ser_data = self.serializer_class(instance=query_related_obj, many=True).data
        ret = {
            'status': True,
            'user': user_obj.username,
            'results': ser_data
        }
        return Response(ret)

    def post(self, request):
        """Fresh user's data, and redirect to get() method"""
        assert self.client_method is not None, ("Must override client_method")
        assert self.model_related_name is not None, ("Must override the model_related_name")

        self.login()
        assert self.client is not None, ("login failed")

        print(getattr(self.client, self.client_method)())
        # self.client.getScores()
        # print("url:", reverse(self.url_related_name))
        # return redirect(to=reverse(self.url_related_name))
        return self.get("")


class UserView(BaseView):
    authentication_classes = [Authentication, ]
    serializer_class = UserModelSerializer

    def get(self, request):
        user_obj = request.user.user
        ser_data = UserModelSerializer(instance=user_obj).data
        ret = {
            'status': True,
            'results': ser_data
        }
        return Response(ret)

    def post(self, request):
        pass


class CETView(BaseView):
    serializer_class = CETModelSerializer
    model_related_name = "cets"
    client_method = "getCET"


class StudentInformationView(BaseView):
    serializer_class = StudentInfoModelSerializer
    model_related_name = "selfInfo"
    client_method = "getStudentInfo"


class ScoreView(BaseView):
    serializer_class = ScoreModelSerializer
    model_related_name = "scores"
    client_method = "getScores"


class ExamPlanView(BaseView):
    serializer_class = ExamPlanModelSerializer
    model_related_name = "exams"
    client_method = "getExamPlan"


class CoursePlanView(BaseView):
    serializer_class = CoursePlanModelSerializer
    model_related_name = "coursesPlan"
    client_method = "getTeachingPlan"


class CourseNowView(BaseView):
    serializer_class = CoursePlanModelSerializer
    model_related_name = "coursesNow"
    client_method = "getClassTable"


class ClassRoomView(APIView):

    def get(self, request):
        query_data = request.GET.get('building')
        class_obj = ClassRoom.objects.all()
        ser_data = ClassRoomModelSerializer(instance=class_obj, many=True).data
        return Response(ser_data)

    # @api_view('GET')
    # def query_class_room():
    #     queryset = ClassRoom.objects.all()
    #     serializer_class = ClassRoomModelSerializer
    #     pass
