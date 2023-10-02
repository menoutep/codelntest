from rest_framework import serializers
from base.models import UserBadge, Badge
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class UserBadgeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    badge = BadgeSerializer()

    class Meta:
        model = UserBadge
        fields = '__all__'
