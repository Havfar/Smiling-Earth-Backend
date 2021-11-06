from challenges.models import Challenge
from django.contrib.auth import get_user_model
from django.db import models
from posts.models import Comment, Like, Post
from users.models import Follower


class Notification(models.Model):
    notification_type = models.IntegerField()
    from_user = models.ForeignKey(get_user_model(
    ), on_delete=models.CASCADE, related_name='notification_from', null=True)
    to_user = models.ForeignKey(get_user_model(
    ), on_delete=models.CASCADE,     related_name='notification_to', null=True)
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

    class Meta:
        ordering = ['-timestamp']
