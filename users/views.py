from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from notifications.models import Notification
from rest_framework import generics, permissions, response, status

from users.models import Follower, Profile, User
from users.permissions import IsFollowingOrOwner, IsOwner
from users.serializers import (AvatarSerializer, FollowerSerializer,
                               FollowingSerializer,
                               MyProfileDetailedSerializer,
                               ProfileDetailedSerializer, ProfileSerializer)


class UserList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserSelfDetail(generics.ListAPIView):
    serializer_class = MyProfileDetailedSerializer

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user.pk)


class UserDetail(generics.RetrieveAPIView):
    serializer_class = ProfileDetailedSerializer
    queryset = Profile.objects.all()
    # permission_classes = [permissions.IsAuthenticated and IsFollowingOrOwner]


class Following(generics.ListAPIView):
    serializer_class = FollowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # user = get_object_or_404(Follower, pk=self.kwargs["pk"])
        return Follower.objects.filter(is_followed_by=self.request.user)


class UpdateAvatar(generics.UpdateAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.pk)
        # self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(status=status.HTTP_200_OK, data={"message": "avatar updated successfully"})

        else:
            return response.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"message": "failed", "details": serializer.errors})


class Followers(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # user = get_object_or_404(User, pk=self.kwargs["pk"])
        # return Follower.objects.filter(user=self.request.user).exclude(is_followed_by=self.request.user)
        return Follower.objects.filter(Q(user=self.request.user))


class NotFollowingList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        followers = Follower.objects.filter(
            Q(is_followed_by=self.request.user))
        users = [follower.user.id for follower in followers]

        return Profile.objects.filter(~Q(user_id__in=users), ~Q(user_id=self.request.user.id))


@login_required
def follow(request, pk):
    user = get_object_or_404(User, pk=pk)
    already_followed = Follower.objects.filter(
        user=user, is_followed_by=request.user).first()

    if not already_followed:
        new_follower = Follower(user=user, is_followed_by=request.user)
        new_follower.save()
        Notification.objects.create(
            from_user=request.user, to_user=user, notification_type=3, follow=new_follower)
        follower_count = Follower.objects.filter(user=user).count()
        return JsonResponse({'status': 'Following', 'count': follower_count})

    already_followed.delete()
    follower_count = Follower.objects.filter(user=user).count()
    return JsonResponse({'status': 'Not following', 'count': follower_count})
