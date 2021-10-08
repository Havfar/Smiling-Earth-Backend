from rest_framework import serializers

from challenges.models import Challenge, ChallengeUser


class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'symbol', 'background_color']


class ChallengeDetailedSerializer(serializers.HyperlinkedModelSerializer):
    leaderboard = serializers.ReadOnlyField(source='get_leaderboard')

    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description',
                  'symbol', 'background_color', 'leaderboard']


class ChallengeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeUser
        fields = ['id', 'score', 'progress']
