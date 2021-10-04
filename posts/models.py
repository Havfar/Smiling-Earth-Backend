from activities.models import Activity
from activities.serializers import ActivitySerializer, ActivitySerializerGet
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from teams.models import Team
from users.models import Profile
from users.serializers import ProfileSerializer


class Post(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="posts"
    )
    content = models.CharField(max_length=300)
    activity = models.ForeignKey(
        Activity, default=None, null=True, on_delete=models.CASCADE, related_name="posts"
    )
    team = models.ForeignKey(
        Team, default=None, null=True, on_delete=models.CASCADE, related_name='posts')

    def get_likes_count(self):
        return Like.objects.filter(post=self).count()

    def get_likes(self):
        likes = Like.objects.filter(post=self)
        serializer = _LikesSerializer(instance=likes, many=True)
        return serializer.data

    def get_comments_count(self):
        return Comment.objects.filter(post=self).count()

    def get_comments(self):
        comments = Comment.objects.filter(post=self)
        serializer = _CommentSerializer(comments, many=True)
        return serializer.data

    def get_owner(self):
        user = Profile.objects.get(user=self.user)
        serializer = ProfileSerializer(instance=user)
        return serializer.data

    def get_activity(self):
        if self.activity != None:
            serializer = ActivitySerializerGet(instance=self.activity)
            return serializer.data
        return None

    class Meta:
        ordering = ['timestamp']


class Like(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="likes"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post")

    def get_owner(self):
        user = Profile.objects.get(user=self.user)
        serializer = ProfileSerializer(instance=user)
        return serializer.data

    # staticmethod getLikes(Post post){
    #     return ""
    # }


class Comment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="comment"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comment")

    content = models.CharField(max_length=300)

    def get_owner(self):
        user = Profile.objects.get(user=self.user)
        serializer = ProfileSerializer(instance=user)
        return serializer.data


# Creating a private like serializer to prevent circular import error
class _LikesSerializer(ModelSerializer):

    user = serializers.ReadOnlyField(source='get_owner')

    class Meta:
        model = Like
        depth = 1
        fields = ['id', 'user', 'timestamp']


class _CommentSerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source='get_owner')

    class Meta:
        depth = 1
        model = Comment
        fields = ['id', 'user', 'timestamp', 'content']
