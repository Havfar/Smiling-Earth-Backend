from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework import permissions
from users.serializers import UserSerializer, UserDetailedSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, mixins


class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailedSerializer

# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]