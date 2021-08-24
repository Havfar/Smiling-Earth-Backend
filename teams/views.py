from django.http import request
from teams.serializers import LeaveTeamSerializer, MemberSerializer, RivalSerializer, TeamDetailSerializer, TeamSerializer, JoinTeamSerializer
from teams.models import Rival, Team
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, serializers, mixins, status
from teams.models import Team, Member
from django.db.models import Q
from users.permissions import IsOwner

class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.filter(is_public = True)
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class MembersOfTeam(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        team = get_object_or_404(Team, pk = self.kwargs["pk"])
        return Member.objects.filter(team = team)
    
class Join(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = JoinTeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class Leave(mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = LeaveTeamSerializer
    queryset = Member.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class Rivals(generics.ListCreateAPIView, generics.UpdateAPIView):
    serializer_class = RivalSerializer
    queryset = Rival.objects.filter(status = 'a')
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team = get_object_or_404(Team, pk = self.kwargs["pk"])
        return Rival.objects.filter(Q(sender=team) | Q(receiver=team), Q(status='a'))

class RivalRequests(generics.RetrieveUpdateAPIView):
    serializer_class = RivalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team = get_object_or_404(Team, pk = self.kwargs["pk"])
        return Rival.objects.filter(Q(receiver=team), Q(status='p'))

