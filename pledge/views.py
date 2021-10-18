from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from teams.models import Team
from users.permissions import IsFollowingOrOwner

from pledge.models import Pledge, TeamPledge, UserPledge
from pledge.permissions import IsOwner
from pledge.serializers import (PledgeSerializer, TeamPledgeSerializer,
                                UserPledgeSerializer)


class PledgeList(generics.ListAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    permission_classes = [permissions.IsAuthenticated]


class PledgeUserList(generics.ListAPIView):
    serializer_class = UserPledgeSerializer
    # permission_classes = [permissions.IsAuthenticated and IsFollowingOrOwner]

    def get_queryset(self):
        user = get_object_or_404(get_user_model(), pk=self.kwargs['pk'])
        return UserPledge.objects.filter(user=user)

class MyPledgeUserList(generics.ListAPIView):
    serializer_class = UserPledgeSerializer
    # permission_classes = [permissions.IsAuthenticated and IsFollowingOrOwner]

    def get_queryset(self):
        user = self.request.user
        return UserPledge.objects.filter(user=user)


class PledgeTeamList(generics.ListAPIView):
    serializer_class = TeamPledgeSerializer
    # permission_classes = [permissions.IsAuthenticated and IsFollowingOrOwner]

    def get_queryset(self):
        team = get_object_or_404(Team, pk=self.kwargs['pk'])
        return TeamPledge.objects.filter(team=team)


class CreatePledgeUser(generics.CreateAPIView):
    serializer_class = UserPledgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_pledge, created = UserPledge.objects.get_or_create(
            user=request.user, pledge=request.data['pledge'])
        return Response(status=status.HTTP_201_CREATED, data={'user_pledge': {"id": user_pledge.id, 'pledge': user_pledge.pledge.id}})


class PledgeUserDelete(generics.DestroyAPIView):
    serializer_class = UserPledgeSerializer
    permission_classes = [permissions.IsAuthenticated and IsOwner]
