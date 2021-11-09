from challenges.models import Challenge
from django.contrib.auth import get_user_model
from django.core.checks import messages
from django.db import models
from posts.models import Comment, Like, Post
from users.models import Follower, Profile
from users.serializers import ProfileSerializer


class Notification(models.Model):
    # 0 = comment, 1 = like, 2 = challenge, 3 = follow
    notification_type = models.IntegerField()
    from_user = models.ForeignKey(get_user_model(
    ), on_delete=models.CASCADE, related_name='notification_from', null=True)
    to_user = models.ForeignKey(get_user_model(
    ), on_delete=models.CASCADE,     related_name='notification_to', null=True)
    message = models.CharField(max_length=200)
    post = models.ForeignKey(
        Post, related_name='+', on_delete=models.CASCADE, null=True, blank=True)
    like = models.ForeignKey(Like, related_name='+',
                             on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(
        Comment, related_name='+', on_delete=models.CASCADE, null=True, blank=True)
    challenge = models.ForeignKey(
        Challenge, related_name='+', on_delete=models.CASCADE, null=True, blank=True)
    follow = models.ForeignKey(
        Follower, related_name='+', on_delete=models.CASCADE, null=True, blank=True)
    user_has_seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_from_user(self):
        if self.from_user != None:

            user = Profile.objects.get(user=self.from_user)
            serializer = ProfileSerializer(many=False, instance=user)
            return serializer.data
        return None

    class Meta:
        ordering = ['-timestamp']
