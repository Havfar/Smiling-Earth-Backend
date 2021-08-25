from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics, permissions

from users.models import Follower, Profile, User
from users.permissions import IsFollowingOrOwner, IsOwner
from users.serializers import (FollowerSerializer, ProfileDetailedSerializer,
                               ProfileSerializer)


class UserList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveAPIView):
    serializer_class = ProfileDetailedSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated and IsFollowingOrOwner]


class Following(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated and IsOwner]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        return Follower.objects.filter(is_followed_by=user)


class Followers(generics.ListAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated and IsOwner]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        return Follower.objects.filter(user=user).exclude(is_followed_by=user)


@login_required
def follow(request, pk):
    user = get_object_or_404(User, pk=pk)
    already_followed = Follower.objects.filter(
        user=user, is_followed_by=request.user).first()

    if not already_followed:
        new_follower = Follower(user=user, is_followed_by=request.user)
        new_follower.save()
        follower_count = Follower.objects.filter(user=user).count()
        return JsonResponse({'status': 'Following', 'count': follower_count})

    already_followed.delete()
    follower_count = Follower.objects.filter(user=user).count()
    return JsonResponse({'status': 'Not following', 'count': follower_count})
