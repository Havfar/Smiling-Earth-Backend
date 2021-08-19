from django.shortcuts import render
from rest_framework import generics, mixins
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.parsers import JSONParser
from posts.models import Comment, Like, Post
from rest_framework import permissions
from posts.serializers import CommentSerializer, LikeSerializer, PostSerializer, CommentPostSerializer, LikePostSerializer
from rest_framework.filters import OrderingFilter

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

#TODO: Slett listView
class Likes(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikePostSerializer

class LikeList(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk = self.kwargs["pk"])
        return Like.objects.filter(Q(post=post))

# TODO: Slett listView
class Comments (generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentPostSerializer

class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk = self.kwargs["pk"])
        return Comment.objects.filter(Q(post=post))