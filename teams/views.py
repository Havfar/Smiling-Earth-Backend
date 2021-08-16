from teams.serializers import MemberSerializer, TeamDetailSerializer, TeamSerializer
from teams.models import Team
from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers
from teams.models import Team, Member

class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.filter(is_public = True)
    # members_count = serializers.IntegerField(source = 'get_followers_count')
    serializer_class = TeamSerializer


class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer

class MembersOfTeam(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    def get_queryset(self):
        team = get_object_or_404(Team, pk = self.kwargs["pk"])
        return Member.objects.all()
        # return Member.objects.filter(team = team)
