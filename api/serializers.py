from rest_framework.serializers import ModelSerializer

from api import models


class ScoreModelSerializer(ModelSerializer):
    class Meta:
        model = models.Score
        fields = '__all__'


class CETModelSerializer(ModelSerializer):
    class Meta:
        model = models.CET
        exclude = ['id']

    def to_representation(self, instance):
        ret = {
            'level': instance.level,
            'date': instance.date,
            'score': instance.score,
        }
        return ret


class ExamPlanModelSerializer(ModelSerializer):
    class Meta:
        model = models.ExamPlan
        fields = '__all__'


class CoursePlanModelSerializer(ModelSerializer):
    class Meta:
        model = models.TeachingPlanCourse
        fields = '__all__'


class CourseNowModelSerializer(ModelSerializer):
    class Meta:
        model = models.ClassCourse
        fields = '__all__'


class TeachingPlanCourseModelSerializer(ModelSerializer):
    class Meta:
        model = models.TeachingPlanCourse
        fields = '__all__'


class StudentInfoModelSerializer(ModelSerializer):
    class Meta:
        model = models.StudentInfo
        fields = '__all__'


class ClassRoomModelSerializer(ModelSerializer):
    class Meta:
        model = models.ClassRoom
        fields = '__all__'


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'latest_GPA', 'latest_login')
