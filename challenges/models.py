from django.db import models
from rest_framework import serializers
from teams.models import Rival, Team
from teams.serializers import TeamSerializer
from teams.views import Rivals
from users.models import Profile, User
from users.serializers import ProfileSerializer


class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    symbol = models.CharField(max_length=12)
    background_color = models.CharField(max_length=12)
    goal = models.IntegerField(default=0)
    is_team_challenge = models.BooleanField(default=False)
    challenge_type = models.IntegerField(default=0)
    challenge_type_feature = models.CharField(max_length=12, default='')

    def get_leaderboard(self):
        if self.is_team_challenge:
            teams_qs = ChallengeTeam.objects.filter(
                challenge=self).order_by('-score')
            teams = _ChallengeTeamSerializer(instance=teams_qs, many=True)
            return teams.data

        users_qs = ChallengeUser.objects.filter(
            challenge=self).order_by('-score')
        users = _ChallengeUserSerializer(instance=users_qs, many=True)
        return users.data

    def get_challenge_type_feature(self):
        features = []
        for i in self.challenge_type_feature.split(','):
            if i != '':
                features.append(int(i))
        return features


class ChallengeUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='challenge_user')
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE, related_name='challenge_challenge')
    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(auto_created=True, default=0)
    progress = models.IntegerField(auto_created=True, default=0)

    def get_user_profile(self):
        user = Profile.objects.get(user=self.user)
        serializer = ProfileSerializer(many=False, instance=user)

        return serializer.data


class ChallengeTeam(models.Model):
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='challenge_team')
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE, related_name='challenge_challenge_team')
    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(auto_created=True, default=0)
    progress = models.IntegerField(auto_created=True, default=0)


# Private serializer to prevent circular import error
class _ChallengeUserSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='get_user_profile')

    class Meta:
        model = ChallengeUser
        fields = ['id', 'user', 'score', 'progress']

# Private serializer to prevent circular import error


class _ChallengeTeamSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='get_user_profile')
    team = TeamSerializer(read_only=True)

    class Meta:
        model = ChallengeUser
        fields = ['id', 'team', 'score', 'progress']
