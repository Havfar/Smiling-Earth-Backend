from django.contrib.auth import get_user_model
from django.http import request
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from pledge.models import Pledge, UserPledge
from pledge.serializers import PledgeSerializer, UserPledgeSerializer
from pledge.permissions import IsOwner
from users.permissions import IsFollowingOrOwner

class PledgeList(generics.ListAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PledgeUserList(generics.ListAPIView):
    serializer_class =  UserPledgeSerializer
    permission_classes = [permissions.IsAuthenticated and IsFollowingOrOwner]

    def get_queryset(self):
        user = get_object_or_404(get_user_model(), pk = self.kwargs['pk'])
        return UserPledge.objects.filter(user = user);

class CreatePledgeUser(generics.CreateAPIView):
    serializer_class =  UserPledgeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        user_pledge, created = UserPledge.objects.get_or_create(user = request.user, pledge = request.data['pledge'])
        return Response(status=status.HTTP_201_CREATED,data={'user_pledge': {"id" : user_pledge.id, 'pledge': user_pledge.pledge.id}})


class PledgeUserDelete(generics.DestroyAPIView):
    serializer_class = UserPledgeSerializer
    permission_classes = [permissions.IsAuthenticated and IsOwner]

