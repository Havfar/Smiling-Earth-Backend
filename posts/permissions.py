from users.models import Follower, User
from posts.models import Post
from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsAllowedToViewPost(permissions.BasePermission): 

    def has_permission(self, request, view):
        user = User.objects.get(id=request.data["user"])
        post = Post.objects.get(id=request.data["post"])

        followers_queryset = Follower.objects.filter(is_followed_by = user)
        followers = [ user.id for user in followers_queryset ]

        author = post.user.id
        return author in followers

    def has_object_permission(self, request, view, obj):
        followers_queryset = Follower.objects.filter(is_followed_by = request.user)
        followers = [ user for user in followers_queryset ]
        author = obj.post.user
        return False
