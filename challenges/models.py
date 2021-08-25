from django.db import models
from users.models import User


class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class ChallengeUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='challenge_user')
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE, related_name='challenge_challenge')
    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(auto_created=True, default=0)
    progress = models.IntegerField(auto_created=True, default=0)
