import datetime

from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from emissions.models import Emission
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from users.models import User
from users.permissions import IsOwner

from teams.models import Member, Rival, Team
from teams.permissions import IsTeamAdmin
from teams.serializers import (JoinTeamSerializer, LeaveTeamSerializer,
                               MemberEmissionsSerializer, MemberSerializer,
                               RivalSerializer, TeamDetailSerializer,
                               TeamSerializer, UserTeamSerializer)


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
    permission_classes = [permissions.IsAuthenticated]
    queryset = Emission.objects.all()

    def get(self, request, *args, **kwargs):
        team = get_object_or_404(Team, pk=self.kwargs["pk"])
        members = Member.objects.filter(team=team)
        members_ids = [member.user.pk for member in members]
        emissions = Emission.objects.filter(Q(user__in=members_ids))
        transportEmission = 0
        energyEmission = 0
        for emission in emissions:
            if emission.isSourceTransport:
                transportEmission += emission.emissions
            else:
                energyEmission += emission.emissions
        return Response(data={"transport": transportEmission, "energy": energyEmission})


class TeamEmissionsThisWeek(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Emission.objects.all()

    def get(self, request, *args, **kwargs):
        team = get_object_or_404(Team, pk=self.kwargs["pk"])
        members = Member.objects.filter(team=team)
        members_ids = [member.user.pk for member in members]
        today = datetime.date.today()
        year, week_num, day_of_week = today.isocalendar()
        emissions = Emission.objects.filter(
            Q(user__in=members_ids), Q(weekNo=week_num))
        transportEmission = 0
        energyEmission = 0
        for emission in emissions:
            if emission.isSourceTransport:
                transportEmission += emission.emissions
            else:
                energyEmission += emission.emissions
        return Response(data={"transport": transportEmission, "energy": energyEmission})


class MembersOfTeam(generics.ListCreateAPIView):
    serializer_class = MemberEmissionsSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team = get_object_or_404(Team, pk=self.kwargs["pk"])
        return Member.objects.filter(team=team)


class UserTeamList(generics.ListAPIView):
    serializer_class = UserTeamSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        return Member.objects.filter(user=user)


class Join(generics.CreateAPIView):
    serializer_class = JoinTeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        team = get_object_or_404(Team, pk=request.data['team'])

        member, created = Member.objects.get_or_create(user=user, team=team)

        return Response(MemberSerializer(instance=member).data, status=status.HTTP_201_CREATED)


class Leave(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        team = get_object_or_404(Team, pk=self.kwargs["pk"])
        user = request.user

        member = get_object_or_404(
            Member, Q(user=user, team=team))
        member.delete()
        # Member.objects.delete(Q(user=request.user, team=request.data['team']))
        return Response(status=status.HTTP_200_OK)


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
