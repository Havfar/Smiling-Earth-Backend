from django.contrib.auth import get_user_model
from django.db.models import fields
from rest_framework import serializers
from users.models import Follower, Profile

class UserSerializer(serializers.ModelSerializer):
    # TODO: Legg til profil ID
    class Meta:
        model = get_user_model()
        fields = ['id'] 

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'user']

class ProfileDetailedSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source = 'get_followers_count')
    email = serializers.CharField(source='get_email')
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'followers_count', 'email']

class FollowerSerializer(serializers.ModelSerializer):
    user = serializers.DictField(child = serializers.CharField(), source = 'get_user_info', read_only = True)
    # is_followed_by = serializers.DictField(child = serializers.CharField(), source = 'get_is_followed_by_info', read_only = True)

    class Meta:
        model = Follower
        fields = ['user']
        read_only_fields = ['user']
