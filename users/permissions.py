from rest_framework import permissions

from users.models import Follower


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsFollowingOrOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        followers_queryset = Follower.objects.filter(
            is_followed_by=request.user)
        followers = [user.id for user in followers_queryset]
        requested_user_id = view.kwargs['pk']
        return requested_user_id in followers or requested_user_id == request.user.id

    def has_object_permission(self, request, view, obj):
        followers_queryset = Follower.objects.filter(
            is_followed_by=request.user)
        followers = [user.id for user in followers_queryset]
        return obj.user.id in followers or obj.user == request.user
