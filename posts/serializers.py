from challenges.serializers import ChallengeSerializer
from django.apps import apps
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Comment, Like, Post


class PostSerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source="get_owner")
    content = serializers.CharField()
    likes_count = serializers.ReadOnlyField(source="get_likes_count")
    comments_count = serializers.ReadOnlyField(source="get_comments_count")
    activity = serializers.ReadOnlyField(source="get_activity", required=False)
    challenge = ChallengeSerializer(read_only=True)

    class Meta:
        depth = 1
        model = Post
        fields = ["id", "user", "content", "timestamp",
                  "likes_count", "comments_count", "activity", "challenge", "team_id"]


class PostDetailedSerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source="get_owner")
    content = serializers.CharField()
    likes = serializers.ReadOnlyField(source="get_likes")
    comments = serializers.ReadOnlyField(source="get_comments")
    activity = serializers.ReadOnlyField(source="get_activity", required=False)
    challenge = ChallengeSerializer(read_only=True)

    class Meta:
        depth = 1
        model = Post
        fields = ["id", "user", "content", "timestamp",
                  "likes", "comments", "activity", "challenge"]


class LikesSerializer(ModelSerializer):

    user = serializers.ReadOnlyField(source="get_owner")
    post = serializers.ReadOnlyField(source="post.id")

    class Meta:
        model = Like
        depth = 1
        fields = ["id", "user", "post", "timestamp"]


class LikePostSerializer(ModelSerializer):

    class Meta:
        model = Like
        depth = 1

        fields = ["id", "user", "post", "timestamp"]


class LikesLikedSerializer(ModelSerializer):
    class Meta:
        model = Like
        depth = 1
        fields = ["id", "user_id", "post_id", ]


class LikePostResponseSerializer(ModelSerializer):

    class Meta:
        model = Like

        fields = ["id", "user", "post"]


class CommentSerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source="get_owner")
    # post = serializers.ReadOnlyField(source="post.id")

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)

    class Meta:
        depth = 1
        model = Comment
        fields = ["id", "user", "post", "timestamp", "content"]


class CommentPostSerializer(ModelSerializer):

    post = serializers.ReadOnlyField(source="post.id")

    class Meta:
        depth = 1
        model = Comment
        fields = ["id", "user", "post", "timestamp", "content"]
