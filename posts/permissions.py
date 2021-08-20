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

        followersQueryset = Follower.objects.filter(is_followed_by = user)
        followers = [ user.id for user in followersQueryset ]

        author = post.user.id
        return author in followers

    def has_object_permission(self, request, view, obj):
        followersQueryset = Follower.objects.filter(is_followed_by = request.user)
        followers = [ user for user in followersQueryset ]
        author = obj.post.user
        return False
