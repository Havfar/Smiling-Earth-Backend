from rest_framework import serializers

from challenges.models import Challenge, ChallengeUser


class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    feature_list = serializers.ReadOnlyField(
        source='get_challenge_type_feature')

    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description',
                  'symbol', 'background_color', 'goal', 'challenge_type', 'feature_list']


class ChallengeDetailedSerializer(serializers.HyperlinkedModelSerializer):
    leaderboard = serializers.ReadOnlyField(source='get_leaderboard')

    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description',
                  'symbol', 'background_color', 'leaderboard']


class ChallengeUserSerializer(serializers.ModelSerializer):
    challenge = ChallengeSerializer(read_only=True)

    class Meta:
        model = ChallengeUser
        fields = ['id', 'score', 'progress', 'challenge']


class ChallengeUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChallengeUser
        fields = ['score', 'progress', ]
