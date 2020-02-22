from django.urls import path, include
from rest_framework import routers

from api.views import UserViewSet, ClassRoomViewSet

router = routers.SimpleRouter()
router.register('users', UserViewSet, basename='user')
router.register('rooms', ClassRoomViewSet, basename='class-room')
# router.register('cets', CETViewSet, basename='cet')


urlpatterns = [
    path('', include(router.urls)),
]
