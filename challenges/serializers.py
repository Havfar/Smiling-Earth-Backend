from rest_framework import serializers
from challenges.models import Challenge, ChallengeUser


class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'start_date', 'end_date']


class ChallengeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeUser
        fields = ['id', 'user', 'challenge', 'score', 'progress']


class UserInChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeUser
        fields = ['user', 'score', 'progress']
