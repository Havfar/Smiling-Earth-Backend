from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
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


class NotPledgeUserList(generics.ListAPIView):
    serializer_class = PledgeSerializer

    # permission_classes = [permissions.IsAuthenticated and IsFollowingOrOwner]

    def get_queryset(self):
        user = self.request.user
        user_pledges_qs = UserPledge.objects.filter(user=user)
        selected_pledges_id = [pledge.pledge.id for pledge in user_pledges_qs]
        return Pledge.objects.filter(
            ~Q(id__in=selected_pledges_id))


class GetAllAndMyPledgeUserList(generics.ListAPIView):
    serializer_class = PledgeSerializer

    # permission_classes = [permissions.IsAuthenticated and IsFollowingOrOwner]
    def get(self, request, *args, **kwargs):
        user = self.request.user
        #  user_challenges_qs = ChallengeUser.objects.filter(Q(user=user))
        # user_challenges = [
        #     challenge for challenge in user_challenges_qs]

        user_pledges_qs = UserPledge.objects.filter(user=user)
        selected_pledges_id = [pledge.id for pledge in user_pledges_qs]
        selected_pledges = [pledge for pledge in user_pledges_qs]
        un_selected_pledges = Pledge.objects.filter(
            ~Q(id__in=selected_pledges_id))
        # pledges = selected_pledges + un_selected_pledges
        serializer = PledgeSerializer(selected_pledges, many=True)
        serializer1 = PledgeSerializer(un_selected_pledges, many=True)
        return JsonResponse({'data': serializer.data})

        # return Response(status=status.HTTP_200_OK, data={"selected": PledgeSerializer(data=selected_pledges), "unSelected": PledgeSerializer(data=un_selected_pledges)})


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
        pledges = []
        body = request.data['pledges']
        user_pledges = [i.strip()
                        for i in body[1:-1].replace('"', "").split(',')]

        for user_pledge in user_pledges:
            pledge = get_object_or_404(Pledge, pk=user_pledge)
            pledges.append(UserPledge(user=request.user, pledge=pledge))
        UserPledge.objects.bulk_create(pledges)
        # user_pledge, created = UserPledge.objects.get_or_create(
        #     user=request.user, pledge=request.data['pledge'])
        return Response(status=status.HTTP_201_CREATED)


class PledgeUserDelete(generics.DestroyAPIView):
    serializer_class = UserPledgeSerializer
    permission_classes = [permissions.IsAuthenticated and IsOwner]

    def destroy(self, request, *args, **kwargs):
        pledge = get_object_or_404(Pledge, pk=self.kwargs["pk"])
        user = request.user

        user_pledges = UserPledge.objects.filter(
            Q(user=user, pledge=pledge))
        for user_pledge in user_pledges:
            user_pledge.delete()
        return Response(status=status.HTTP_200_OK)
