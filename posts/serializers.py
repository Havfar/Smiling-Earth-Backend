from django.apps import apps
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Comment, Like, Post


class PostSerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source="get_owner")
    content = serializers.CharField()
    likes_count = serializers.ReadOnlyField(source='get_likes_count')
    comments_count = serializers.ReadOnlyField(source='get_comments_count')

    class Meta:
        depth = 1
        model = Post
        fields = ['id', 'user', 'content', 'timestamp',
                  'likes_count', 'comments_count']


class PostDetailedSerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source="get_owner")
    content = serializers.CharField()
    likes = serializers.ReadOnlyField(source='get_likes')
    comments = serializers.ReadOnlyField(source='get_comments')

    class Meta:
        depth = 1
        model = Post
        fields = ['id', 'user', 'content', 'timestamp', 'likes', 'comments']


class LikesSerializer(ModelSerializer):

    user = serializers.ReadOnlyField(source='get_owner')
    # post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Like
        depth = 1
        fields = ['id', 'user', 'post', 'timestamp']


class LikePostSerializer(ModelSerializer):

    class Meta:
        model = Like
        depth = 1

        fields = ['id', 'user', 'post', 'timestamp']


class CommentSerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source='get_owner')
    # post = serializers.ReadOnlyField(source='post.id')

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)

    class Meta:
        depth = 1
        model = Comment
        fields = ['id', 'user', 'post', 'timestamp', 'content']


class CommentPostSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = Comment
        fields = ['id', 'user', 'post', 'timestamp', 'content']
