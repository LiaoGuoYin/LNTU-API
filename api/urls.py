from django.urls import path, include
from rest_framework import routers

from api.views import ScoreViewSet, CETViewSet, UserViewSet

router = routers.SimpleRouter()
router.register('scores', ScoreViewSet)
router.register('cets', CETViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
