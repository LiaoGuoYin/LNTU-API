from django.urls import path

from api.views import CETView, StudentInformationView, ScoreView, ExamPlanView, CoursePlanView, CourseNowView, AuthView, \
    ClassRoomView

urlpatterns = [
    path('class-room', ClassRoomView.as_view(), name='room'),
    path('login/', AuthView.as_view(), name='auth'),
    # path('user/account', AccountView.as_view(), name='account'),
    path('user/info', StudentInformationView.as_view(), name='information'),
    path('user/cet', CETView.as_view(), name='cet'),
    path('user/score', ScoreView.as_view(), name='score'),
    path('user/exam-plan', ExamPlanView.as_view(), name='examPlan'),
    path('user/course-plan', CoursePlanView.as_view(), name='coursePlan'),
    path('user/course-now', CourseNowView.as_view(), name='courseNow'),  # TODO 合并
]
