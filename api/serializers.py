from rest_framework import serializers

from web.models import Score, CET, User


class ScoreSerializer(serializers.ModelSerializer):
    # url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Score
        fields = '__all__'


class CETSerializer(serializers.ModelSerializer):
    class Meta:
        model = CET
        exclude = ['id']


class UserSerializer(serializers.ModelSerializer):
    cet = CETSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'
        # fields = ['username', 'password', 'cet']
        # exclude = ['id']
