from django.db.models import Q
from django.http import request
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from teams.models import Team
from users.models import Follower, User

from posts.models import Comment, Like, Post
from posts.permissions import IsAllowedToViewPost, IsOwner
from posts.serializers import (CommentPostSerializer, CommentSerializer,
                               LikePostResponseSerializer, LikePostSerializer,
                               LikesLikedSerializer, LikesSerializer,
                               PostDetailedSerializer, PostSerializer)


class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return get_posts_queryset(self.request.user)

    def perform_create(self, serializer):
        if self.request.data['team_id'] is not None:
            team = get_object_or_404(Team, pk=self.request.data['team_id'])
            serializer.save(user=self.request.user, team=team)
        else:
            serializer.save(user=self.request.user)


class TeamPostList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        team = get_object_or_404(Team, pk=self.kwargs['pk'])
        return Post.objects.filter(Q(team=team))


class UserPostList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return Post.objects.filter(Q(user=user))


class MyPostList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(Q(user=user))


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsOwner]
    queryset = Post.objects.all()
    serializer_class = PostDetailedSerializer


class Liked(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikesLikedSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        user = self.request.user
        return Like.objects.filter(post=post, user=user)


class Likes(generics.CreateAPIView):
    # permission_classes = [permissions.IsAuthenticated, IsAllowedToViewPost]
    serializer_class = LikePostSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        post = get_object_or_404(Post, pk=request.data['post'])
        like, created = Like.objects.get_or_create(user=user, post=post)
        if created:
            Notification.objects.create(notification_type=1, from_user=user,
                                        to_user=post.user, post=post, message='new like', like=like)
        return Response(LikesSerializer(instance=like).data, status=status.HTTP_201_CREATED)


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
        queryset = Like.objects.filter(id=self.kwargs["pk"])
        return queryset

    # def destroy(self, request, *args, **kwargs):
    #     try:
    #         post = get_object_or_404(Post, pk=self.kwargs["pk"])
    #         user = request.user
    #         l = Like.objects.filter(
    #             user=self.request.user, post=post)
    #         like = get_object_or_404(Like, post=post, user=user)
    #         self.perform_destroy(like)
    #     except e:
    #         pass

    #     return Response(status=status.HTTP_204_NO_CONTENT)


class NewComment (generics.CreateAPIView):
    # permission_classes = [permissions.IsAuthenticated and IsAllowedToViewPost]
    serializer_class = CommentPostSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        post = get_object_or_404(Post, pk=request.data['post'])

        content = request.data['content']

        comment = Comment.objects.create(user=user, post=post, content=content)
        Notification.objects.create(notification_type=0, from_user=user,
                                    to_user=post.user, post=post, message='new comment', comment=comment)
        return Response(CommentSerializer(instance=comment).data, status=status.HTTP_201_CREATED)


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
    followers_qs = [user.pk for user in followers]
    followers_qs.append(user.pk)
    # Todo: legg inn user i queryset
    queryset = Post.objects.filter(
        Q(user__pk__in=followers_qs),
        Q(team_id=None)
    )
    return queryset
