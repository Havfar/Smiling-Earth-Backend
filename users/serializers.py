from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from users.models import Follower, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_id', 'first_name', 'last_name']


class ProfileDetailedSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='get_followers_count')
    email = serializers.CharField(source='get_email')

    class Meta:
        model = Profile
        fields = ['user_id', 'first_name',
                  'last_name', 'followers_count', 'email']


class FollowerSerializer(serializers.ModelSerializer):
    # user = serializers.DictField(
    #     child=serializers.CharField(), source='get_profile', read_only=True)
    user = ReadOnlyField(source='get_profile')

    class Meta:
        model = Follower
        fields = ['user']
        read_only_fields = ['user']
