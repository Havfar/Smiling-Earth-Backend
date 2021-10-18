from django.db.models.query_utils import Q
from django.shortcuts import render
from rest_framework import generics
from teams.models import Member, Team

from emissions.models import Emission
from emissions.serializers import EmissionSerializer


class UserEmission(generics.ListCreateAPIView, generics.UpdateAPIView):
    serializer_class = EmissionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Emission.objects.filter(Q(user=user))
        return queryset


class TeamEmissions(generics.ListAPIView):
    serializer_class = EmissionSerializer

    def get_queryset(self):
        team = Member.objects.filter(team=self.kwargs['pk'])
        members = [user.user for user in team]
        queryset = Emission.objects.filter(Q(user__in=members))
        return queryset
