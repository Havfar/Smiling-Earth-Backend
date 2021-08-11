from django.db.models import fields
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedRelatedField
from posts.models import Post

class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source = "user.email")
    content = serializers.CharField()
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'timestamp']
