from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from posts.models import Post
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from teams.models import Team
from users.models import User
from users.permissions import IsOwner

import challenges
from challenges.models import Challenge, ChallengeTeam, ChallengeUser
from challenges.serializers import (ChallengeDetailedSerializer,
                                    ChallengeSerializer,
                                    ChallengeTeamSerializer,
                                    ChallengeUserSerializer,
                                    ChallengeUserUpdateSerializer)


class ChallengeList(generics.ListCreateAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        joined_challenges_qs = ChallengeUser.objects.filter(user=user)
        joined_challenges = [
            challenge.challenge.pk for challenge in joined_challenges_qs]
        challenges = Challenge.objects.filter(
            ~Q(id__in=joined_challenges), Q(is_team_challenge=False))
        return challenges


class TeamChallengeList(generics.ListCreateAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team = get_object_or_404(Team, pk=self.kwargs['pk'])
        joined_challenges_qs = ChallengeTeam.objects.filter(team=team)
        joined_challenges = [
            challenge.challenge.pk for challenge in joined_challenges_qs]
        challenges = Challenge.objects.filter(
            ~Q(id__in=joined_challenges), Q(is_team_challenge=True))
        return challenges


class ChallengeUserList(generics.ListCreateAPIView):
    serializer_class = ChallengeUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_challenges_qs = ChallengeUser.objects.filter(Q(user=user))
        user_challenges = [
            challenge for challenge in user_challenges_qs]

        challenges = []
        for challenge in user_challenges:
            if(challenge.progress < challenge.challenge.goal):
                challenges.append(challenge.id)

        return ChallengeUser.objects.filter(Q(id__in=challenges))


class TeamChallengeJoinedList(generics.ListCreateAPIView):
    serializer_class = ChallengeTeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team = get_object_or_404(Team, pk=self.kwargs['pk'])
        team_challenges_qs = ChallengeTeam.objects.filter(Q(team=team))
        team_challenges = [
            challenge for challenge in team_challenges_qs]

        challenges = []
        for challenge in team_challenges:
            if(challenge.progress < challenge.challenge.goal):
                challenges.append(challenge.id)

        return ChallengeTeam.objects.filter(Q(id__in=challenges))


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
            if(challenge.progress >= challenge.challenge.goal):
                challenges.append(challenge.challenge.id)

        return Challenge.objects.filter(Q(id__in=challenges))


class CompletedTeamChallengeList(generics.ListCreateAPIView):
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team = get_object_or_404(Team, pk=self.kwargs['pk'])
        team_challenges_qs = ChallengeTeam.objects.filter(Q(team=team))
        team_challenges = [
            challenge for challenge in team_challenges_qs]

        challenges = []
        for challenge in team_challenges:
            if(challenge.progress >= challenge.challenge.goal):
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
            if(challenge.progress >= challenge.challenge.goal):
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


class ChallengeTeamPost(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChallengeUserSerializer

    def create(self, request, *args, **kwargs):
        challenge = get_object_or_404(Challenge, id=request.data['challenge'])
        team = get_object_or_404(Team, id=request.data['team'])
        challenge_team, created = ChallengeTeam.objects.get_or_create(
            team=team, challenge=challenge, score=0, progress=0)

        if created:
            Post.objects.create(
                user=request.user, content="Joined the challenge", challenge=challenge)
        return Response({"challenge team": {"id": challenge_team.id}}, status=status.HTTP_201_CREATED)


class ChallengeUserUpdateAndDelete(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated and IsOwner]
    serializer_class = ChallengeUserUpdateSerializer
    queryset = ChallengeUser.objects.all()

    def get_object(self):
        obj = get_object_or_404(ChallengeUser, user=self.request.user,
                                challenge_id=self.kwargs['pk'])
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        previous_progress = instance.progress
        instance.score = request.data['score']
        instance.progress = request.data['progress']
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            progress_percentage = instance.progress / instance.challenge.goal
            completed = progress_percentage >= 1
            if completed:
                Post.objects.create(
                    user=request.user, content="Completed the challenge", challenge=instance.challenge)
                Notification.objects.create(notification_type=2,
                                            to_user=self.request.user,

                                            message='You completed the challenge: ' + instance.challenge.title + ' 🎉')
            elif previous_progress/instance.challenge.goal <= 0.9 and progress_percentage > 0.9:
                Notification.objects.create(notification_type=2,
                                            to_user=self.request.user,

                                            message='Your almost finished with the task: ' + instance.challenge.title)
            elif previous_progress/instance.challenge.goal <= 0.5 and progress_percentage > 0.5:
                Notification.objects.create(notification_type=2,
                                            to_user=self.request.user,
                                            message='Your 50% finished with the task: ' + instance.challenge.title)

            return Response({"message": "Challenge user is updated", "challenge_user": {"id": instance.id, "score": instance.score, "progress": instance.progress}}, status=status.HTTP_200_OK)

        return Response({"message": "Could not update challenge", "details": serializer.errors})
