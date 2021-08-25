from rest_framework import permissions
from users.models import Follower, User

from posts.models import Post


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAllowedToViewPost(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        post = Post.objects.get(id=request.data["post"])
        followers_queryset = Follower.objects.filter(
            is_followed_by=request.user)
        followers = [user.id for user in followers_queryset]

        author = post.user.id
        return author in followers
