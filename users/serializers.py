from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from users.models import Follower, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    avatar = ReadOnlyField(source='get_avatar')

    class Meta:
        model = Profile
        fields = ['user_id', 'first_name', 'last_name', 'avatar']


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['topType', 'accessoriesType', 'hairColor', 'facialHairType', 'facialHairColor', 'clotheType', 'eyeType',
                  'eyebrowType', 'mouthType', 'skinColor', 'clotheColor', 'style', 'graphicType']


class MyProfileDetailedSerializer(serializers.ModelSerializer):
    followers_count = ReadOnlyField(source='get_followers_count')
    following_count = ReadOnlyField(source='get_following_count')
    avatar = ReadOnlyField(source='get_avatar')

    class Meta:
        model = Profile
        fields = ['user_id', 'first_name', 'bio',
                  'last_name', 'followers_count', 'following_count', 'avatar']


class ProfileDetailedSerializer(serializers.ModelSerializer):
    avatar = ReadOnlyField(source='get_avatar')

    class Meta:
        model = Profile
        fields = ['user_id', 'first_name', 'bio',
                  'last_name', 'avatar']


class FollowerSerializer(serializers.ModelSerializer):
    # user = serializers.DictField(
    #     child=serializers.CharField(), source='get_profile', read_only=True)
    # user = ReadOnlyField(source='get_profile')
    # is_following = ReadOnlyField(source='is_following')
    followed_by = ReadOnlyField(source='get_followed_by_profile')

    class Meta:
        model = Follower
        fields = ['followed_by', 'is_following']


class FollowingSerializer(serializers.ModelSerializer):
    # user = serializers.DictField(
    #     child=serializers.CharField(), source='get_profile', read_only=True)
    user = ReadOnlyField(source='get_profile')
    # is_following = ReadOnlyField(source='is_following')

    class Meta:
        model = Follower
        fields = ['user']
