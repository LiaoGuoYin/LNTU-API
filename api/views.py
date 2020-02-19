from rest_framework import viewsets

from api.serializers import ScoreSerializer, CETSerializer, UserSerializer
from web.models import Score, CET, User


class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """A simple view for viewing user's scores"""
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = ""


class CETViewSet(viewsets.ReadOnlyModelViewSet):
    """A simple view for viewing cet scores"""
    queryset = CET.objects.all()
    serializer_class = CETSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """A view for viewing user's all scores"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
