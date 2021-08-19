from django.db.models import fields
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedRelatedField, ModelSerializer
from posts.models import Like, Post, Comment

class PostSerializer(HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source = "user.email")
    content = serializers.CharField()
    likes_count = serializers.IntegerField(source = 'get_likes_count')
    comments_count = serializers.IntegerField(source = 'get_comments_count')

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'timestamp', 'likes_count', 'comments_count']

class LikeSerializer(ModelSerializer): 
    user = serializers.ReadOnlyField(source = 'user.email')
    post = serializers.ReadOnlyField(source = 'post.id')
    class Meta: 
        model = Comment
        fields = ['id', 'user', 'post', 'timestamp']

class LikePostSerializer(ModelSerializer): 
    class Meta: 
        model = Comment
        fields = ['id', 'user', 'post', 'timestamp']

class CommentSerializer(ModelSerializer): 
    user = serializers.ReadOnlyField(source = 'user.email')
    post = serializers.ReadOnlyField(source = 'post.id')
    class Meta: 
        model = Comment
        fields = ['id', 'user', 'post', 'timestamp', 'content']

class CommentPostSerializer(ModelSerializer): 
    # user = serializers.ReadOnlyField(source = 'user.email')
    # post = serializers.ReadOnlyField(source = 'post.id')
    # post = serializers.IntegerField(source = 'post.id')
    class Meta: 
        model = Comment
        fields = ['id', 'user', 'post', 'timestamp', 'content']

