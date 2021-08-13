from rest_framework import permissions
from users.serializers import UserSerializer, ProfileDetailedSerializer, FollowerSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from users.models import Follower, Profile, User

class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailedSerializer

class Following(generics.ListCreateAPIView):
    serializer_class = FollowerSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk = self.kwargs["pk"])
        return Follower.objects.filter(is_followed_by = user)

class Followers(generics.ListCreateAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk = self.kwargs["pk"])
        return Follower.objects.filter(user = user).exclude(is_followed_by = user)

@login_required
def follow(request, pk):
    user = get_object_or_404(User, pk = pk)
    already_followed = Follower.objects.filter(user = user, is_followed_by = request.user).first()
    if not already_followed:
        new_follower = Follower(user = user, is_followed_by = request.user)
        new_follower.save()
        follower_count = Follower.objects.filter(user = user).count()
        return JsonResponse({'status': 'Following', 'count': follower_count})
    else:
        already_followed.delete()
        follower_count = Follower.objects.filter(user = user).count()
        return JsonResponse({'status': 'Not following', 'count': follower_count})
    return redirect('/')

# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]