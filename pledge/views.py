from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from pledge.models import Pledge, UserPledge
from pledge.serializers import PledgeSerializer, UserPledgeSerializer

class PledgeList(generics.ListAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer

class PledgeUserList(generics.ListCreateAPIView):
    serializer_class =  UserPledgeSerializer

    def get_queryset(self):
        user = get_object_or_404(get_user_model(), pk = self.request.user.id)
        # user = get_object_or_404(get_user_model(), pk = self.request.user)
        return UserPledge.objects.filter(user=user);

class PledgeUserDelete(generics.DestroyAPIView):
    serializer_class = UserPledgeSerializer

