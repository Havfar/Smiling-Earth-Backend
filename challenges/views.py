from rest_framework.response import Response
import challenges
from django.shortcuts import get_object_or_404, render
from django.views import generic
from challenges.models import Challenge, ChallengeUser
from rest_framework import generics, permissions, status
from challenges.serializers import ChallengeSerializer, ChallengeUserSerializer, UserInChallengeSerializer
from users.permissions import IsOwner

# Create your views here.

class ChallengeList(generics.ListCreateAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChallengeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChallengeUserPost(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChallengeUserSerializer

    def create(self, request, *args, **kwargs):
        challenge = get_object_or_404(Challenge, id = request.data['challenge'])
        challenge_user, created = ChallengeUser.objects.get_or_create(user = request.user, challenge = challenge, score = 0, progress = 0)
        return Response({"challenge user" : {"id" : challenge_user.id}}, status=status.HTTP_201_CREATED)

class ChallengeUserUpdateAndDelete(generics.UpdateAPIView ,generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated and IsOwner]
    serializer_class = ChallengeUserSerializer
    queryset = ChallengeUser.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.score = request.data['score']
        instance.progress = request.data['progress']
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Challenge user is updated", "challenge_user" : {"id":instance.id, "score": instance.score, "progress": instance.progress}}, status=status.HTTP_200_OK)

        else:
            return Response({"message": "Could not update challenge", "details": serializer.errors})
