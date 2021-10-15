from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from posts.models import Post
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from users.models import User
from users.permissions import IsOwner

from challenges.models import Challenge, ChallengeUser
from challenges.serializers import (ChallengeDetailedSerializer,
                                    ChallengeSerializer,
                                    ChallengeUserSerializer)


class ChallengeList(generics.ListCreateAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        joined_challenges_qs = ChallengeUser.objects.filter(user=user)
        joined_challenges = [
            challenge.challenge.pk for challenge in joined_challenges_qs]
        challenges = Challenge.objects.filter(~Q(id__in=joined_challenges))
        return challenges


class ChallengeUserList(generics.ListCreateAPIView):
    serializer_class = ChallengeUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChallengeUser.objects.filter(user=user)


class CompletedChallengeList(generics.ListCreateAPIView):
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        user_challenges_qs = ChallengeUser.objects.filter(Q(user=user))
        user_challenges = [
            challenge for challenge in user_challenges_qs]

        challenges = []
        for challenge in user_challenges:
            if(challenge.progress == challenge.challenge.goal):
                challenges.append(challenge.challenge.id)

        return Challenge.objects.filter(Q(id__in=challenges))


class MyCompletedChallengeList(generics.ListCreateAPIView):
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_challenges_qs = ChallengeUser.objects.filter(Q(user=user))
        user_challenges = [
            challenge for challenge in user_challenges_qs]

        challenges = []
        for challenge in user_challenges:
            if(challenge.progress == challenge.challenge.goal):
                challenges.append(challenge.challenge.id)

        return Challenge.objects.filter(Q(id__in=challenges))


class ChallengeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeDetailedSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChallengeUserPost(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChallengeUserSerializer

    def create(self, request, *args, **kwargs):
        challenge = get_object_or_404(Challenge, id=request.data['challenge'])
        challenge_user, created = ChallengeUser.objects.get_or_create(
            user=request.user, challenge=challenge, score=0, progress=0)

        if created:
            Post.objects.create(
                user=request.user, content="Joined the challenge", challenge=challenge)
        return Response({"challenge user": {"id": challenge_user.id}}, status=status.HTTP_201_CREATED)


class ChallengeUserUpdateAndDelete(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated and IsOwner]
    serializer_class = ChallengeUserSerializer
    queryset = ChallengeUser.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.score = request.data['score']
        instance.progress = request.data['progress']
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Challenge user is updated", "challenge_user": {"id": instance.id, "score": instance.score, "progress": instance.progress}}, status=status.HTTP_200_OK)

        return Response({"message": "Could not update challenge", "details": serializer.errors})
