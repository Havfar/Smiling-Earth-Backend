from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from users.models import Follower

from posts.models import Comment, Like, Post
from posts.permissions import IsAllowedToViewPost, IsOwner
from posts.serializers import (CommentPostSerializer, CommentSerializer,
                               LikePostSerializer, LikesSerializer,
                               PostDetailedSerializer, PostSerializer)


class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return get_posts_queryset(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = Post.objects.all()
    serializer_class = PostDetailedSerializer


class Likes(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAllowedToViewPost]
    serializer_class = LikePostSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        post = request.data['post']
        like, created = Like.objects.get_or_create(user=user, post=post)
        return Response({"Liked": {"id": like.id, "user": like.user.id, "post": like.post.id}}, status=status.HTTP_201_CREATED)


class LikeList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikesSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return Like.objects.filter(Q(post=post))


class LikeDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = LikesSerializer

    def get_queryset(self):
        queryset = Like.objects.filter(
            user=self.request.user, id=self.kwargs['pk'])
        return queryset


class NewComment (generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated and IsAllowedToViewPost]
    serializer_class = CommentPostSerializer


class CommentsDelete (generics.DestroyAPIView):
    permission_classes = [IsOwner and permissions.IsAuthenticated]
    serializer_class = CommentPostSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Comment.objects.filter(
            user=self.request.user, id=self.kwargs['pk'])
        return queryset


class CommentList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return Comment.objects.filter(Q(post=post))


def get_posts_queryset(user):
    follower = Follower.objects.filter(user=user)
    followers = (user for user in follower)
    queryset = Post.objects.filter(
        user__pk__in=[user.pk for user in followers])
    return queryset
