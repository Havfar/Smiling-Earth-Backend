from django.shortcuts import render
from rest_framework import generics, mixins
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from posts.models import Post
from rest_framework import permissions
from posts.serializers import PostSerializer
from rest_framework.filters import OrderingFilter

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer