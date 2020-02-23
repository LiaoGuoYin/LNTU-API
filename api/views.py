import traceback

from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth import Authentication, md5
from api.models import User, UserToken, ClassRoom
from api.serializers import StudentInfoModelSerializer, \
    CETModelSerializer, ScoreModelSerializer, ExamPlanModelSerializer, CoursePlanModelSerializer, \
    ClassRoomModelSerializer, CourseNowModelSerializer
from spider.client import Client


class AuthView(APIView):
    """login authentication"""

    def post(self, request, *args, **kwargs):
        ret = {
            'status': True,
            'msg': 'login failed,please check username and password',
        }
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            client = Client(username=username, password=password)
            user_obj = User.objects.update_or_create(username=username, password=password)[0]
            token = md5(username)
            UserToken.objects.update_or_create(user=user_obj, defaults={'token': token})
            ret = {
                'status': True,
                'msg': 'login success',
            }
        except Exception as e:
            print(traceback.format_exc())
        return Response(ret)

    def get(self, request):
        return Response({
            'status': False,
            'msg': 'Invalid HTTP Method',
        })


class StudentInformationView(APIView):
    authentication_classes = [Authentication, ]

    def get(self, request):
        user_info_obj = request.user.user.info  # 反向获取 user.info
        ser_data = StudentInfoModelSerializer(instance=user_info_obj, many=True).data
        return Response(ser_data)


class ScoreView(APIView):
    authentication_classes = [Authentication, ]

    def get(self, request):
        user_info_obj = request.user.user.scores
        ser_data = ScoreModelSerializer(instance=user_info_obj, many=True).data
        return Response(ser_data)


class ExamPlanView(APIView):
    authentication_classes = [Authentication, ]

    def get(self, request):
        user_info_obj = request.user.user.exam_plans
        ser_data = ExamPlanModelSerializer(instance=user_info_obj, many=True).data
        return Response(ser_data)


class CoursePlanView(APIView):
    authentication_classes = [Authentication, ]

    def get(self, request):
        user_info_obj = request.user.user.course_plans
        ser_data = CoursePlanModelSerializer(instance=user_info_obj, many=True).data
        return Response(ser_data)


class CourseNowView(APIView):
    authentication_classes = [Authentication, ]

    def get(self, request):
        user_info_obj = request.user.user.course_now
        ser_data = CourseNowModelSerializer(instance=user_info_obj, many=True).data
        return Response(ser_data)


class CETView(APIView):
    authentication_classes = [Authentication, ]

    def get(self, request):
        user_info_obj = request.user.user.cets
        ser_data = CETModelSerializer(instance=user_info_obj, many=True).data
        return Response(ser_data)


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
