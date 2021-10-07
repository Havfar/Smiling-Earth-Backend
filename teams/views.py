from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from users.permissions import IsOwner

from teams.models import Member, Rival, Team
from teams.permissions import IsTeamAdmin
from teams.serializers import (JoinTeamSerializer, LeaveTeamSerializer,
                               MemberEmissionsSerializer, MemberSerializer,
                               RivalSerializer, TeamDetailSerializer,
                               TeamSerializer)


# Used to list all teams.
# Currently not in use
class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.filter(is_public=True)
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotJoinedTeamList(generics.ListAPIView):
    def get_queryset(self):
        memberships = Member.objects.filter(user=self.request.user)
        teams = [membership.team.pk for membership in memberships]

        return Team.objects.filter(~Q(id__in=teams), Q(is_public=True))

    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]


class JoinedTeamList(generics.ListAPIView):
    def get_queryset(self):
        memberships = Member.objects.filter(user=self.request.user)
        teams = [membership.team.pk for membership in memberships]
        return Team.objects.filter(id__in=teams)

    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeamDetail(generics.RetrieveUpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamAdmin]


class TeamEmissions(generics.ListAPIView):
    serializer_class = MemberEmissionsSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamAdmin]

    def get_queryset(self):
        team = get_object_or_404(Team, pk=self.kwargs["pk"])
        return Member.objects.filter(team=team)


class MembersOfTeam(generics.ListCreateAPIView):
    serializer_class = MemberEmissionsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team = get_object_or_404(Team, pk=self.kwargs["pk"])
        return Member.objects.filter(team=team)


class Join(generics.CreateAPIView):
    serializer_class = JoinTeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        team = get_object_or_404(Team, pk=request.data['team'])

        member, created = Member.objects.get_or_create(user=user, team=team)

        return Response(MemberSerializer(instance=member).data, status=status.HTTP_201_CREATED)


class Leave(mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = LeaveTeamSerializer
    queryset = Member.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class Rivals(generics.ListCreateAPIView, generics.UpdateAPIView):
    serializer_class = RivalSerializer
    queryset = Rival.objects.filter(status='a')
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team = get_object_or_404(Team, pk=self.kwargs["pk"])
        return Rival.objects.filter(Q(sender=team) | Q(receiver=team), Q(status='a'))


class RivalRequests(generics.RetrieveUpdateAPIView):
    serializer_class = RivalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team = get_object_or_404(Team, pk=self.kwargs["pk"])
        return Rival.objects.filter(Q(receiver=team), Q(status='p'))


# class GetRivalsEmission(generics.ListAPIView):
#     serializer_class = RivalEmissionSerializer

#     def get_queryset(self):
#         team = get_object_or_404(Team, pk=self.kwargs["pk"])
#         return Rival.objects.filter(Q(receiver=team), Q(status='p'))
