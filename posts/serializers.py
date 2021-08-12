from django.db.models import fields
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedRelatedField
from posts.models import Like, Post

class PostSerializer(HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source = "user.email")
    content = serializers.CharField()
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'timestamp']

class LikeSerializer(HyperlinkedModelSerializer): 
    user = serializers.ReadOnlyField(source = 'user.email')
    # post = HyperlinkedRelatedField(
    #     queryset=Post.objects.all(), view_name="like-list"
    # )
    post = serializers.ReadOnlyField(source = 'post.id')


    # post = serializers.ReadOnlyField(source = 'post.id')
    
    class Meta: 
        model = Like
        fields = ['id', 'user', 'post', 'timestamp']
