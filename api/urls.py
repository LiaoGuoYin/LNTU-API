from django.urls import path

from api.views import CETView, StudentInformationView, ScoreView, ExamPlanView, CoursePlanView, CourseNowView, AuthView, \
    ClassRoomView

urlpatterns = [
    path('classRoom', ClassRoomView.as_view(), name='room'),
    path('login', AuthView.as_view(), name='auth'),
    # path('user/self', UserView.as_view(), name='self'),
    path('user/info', StudentInformationView.as_view(), name='selfInfo'),
    path('user/cets', CETView.as_view(), name='cets'),
    path('user/scores', ScoreView.as_view(), name='scores'),
    path('user/exams', ExamPlanView.as_view(), name='examPlans'),
    path('user/coursesPlan', CoursePlanView.as_view(), name='coursePlans'),
    path('user/coursesNow', CourseNowView.as_view(), name='courseNow'),  # TODO 合并
]
