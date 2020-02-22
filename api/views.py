from rest_framework import viewsets

from api.serializers import UserModelSerializer, ClassRoomModelSerializer
from web.models import User, ClassRoom


#
# class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
#     """A simple view for viewing user's scores"""
#     queryset = Score.objects.all()
#     serializer_class = ScoreModelSerializer
#     permission_classes = ""
#
#
# class CETViewSet(viewsets.ReadOnlyModelViewSet):
#     """A simple view for viewing cet scores"""
#     queryset = CET.objects.all()
#     serializer_class = CETModelSerializer
#

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """A view for viewing user's all scores"""
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class ClassRoomViewSet(viewsets.ReadOnlyModelViewSet):
    """A view for query class room"""
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomModelSerializer
