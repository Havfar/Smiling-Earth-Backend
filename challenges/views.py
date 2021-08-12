from challenges.serializers import ChallengeSerializer
from django.shortcuts import render
from challenges.models import Challenge
from rest_framework import generics

# Create your views here.

class ChallengeList(generics.ListCreateAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

class ChallengeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer