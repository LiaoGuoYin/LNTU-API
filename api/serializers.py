from rest_framework.serializers import ModelSerializer

from web import models


class ScoreModelSerializer(ModelSerializer):
    class Meta:
        model = models.Score
        fields = '__all__'

    def to_representation(self, instance):
        instance.__dict__.pop('_state')
        return instance.__dict__


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

    def to_representation(self, instance):
        instance.__dict__.pop('_state')
        return instance.__dict__


class TeachingPlanCourseModelSerializer(ModelSerializer):
    class Meta:
        model = models.TeachingPlanCourse
        fields = '__all__'

    def to_representation(self, instance):
        instance.__dict__.pop('_state')
        return instance.__dict__


class StudentInfoModelSerializer(ModelSerializer):
    class Meta:
        model = models.StudentInfo
        fields = '__all__'

    def to_representation(self, instance):
        instance.__dict__.pop('_state')
        return instance.__dict__


class ClassCourseCourseModelSerializer(ModelSerializer):
    class Meta:
        model = models.ClassCourse
        fields = '__all__'

    def to_representation(self, instance):
        instance.__dict__.pop('_state')
        return instance.__dict__


class ClassRoomModelSerializer(ModelSerializer):
    class Meta:
        model = models.ClassRoom
        fields = '__all__'

    def to_representation(self, instance):
        instance.__dict__.pop('_state')
        return instance.__dict__


class UserModelSerializer(ModelSerializer):
    # cets = CETModelSerializer(many=True)
    # scores = ScoreModelSerializer(many=True)
    # exam_plans = ExamPlanModelSerializer(many=True)
    # course_plans = TeachingPlanCourseModelSerializer(many=True)
    # courses = ClassCourseModelSerializer(many=True)
    infos = StudentInfoModelSerializer(many=True)

    class Meta:
        model = models.User
        fields = ('username', 'latest_GPA', 'latest_login', 'infos')
