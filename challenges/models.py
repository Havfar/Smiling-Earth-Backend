from django.db import models
from rest_framework import serializers
from users.models import Profile, User
from users.serializers import ProfileSerializer


class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    symbol = models.CharField(max_length=12)
    background_color = models.CharField(max_length=12)

    def get_leaderboard(self):
        users_qs = ChallengeUser.objects.filter(
            challenge=self).order_by('-score')
        users = _ChallengeUserSerializer(instance=users_qs, many=True)
        return users.data


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


# Private serializer to prevent circular import error
class _ChallengeUserSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='get_user_profile')

    class Meta:
        model = ChallengeUser
        fields = ['id', 'user', 'score', 'progress']
