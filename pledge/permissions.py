
from rest_framework import permissions
from users.models import Follower

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
