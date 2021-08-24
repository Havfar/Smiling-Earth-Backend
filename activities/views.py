from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from activities.models import Activity, ActivityTag
from activities.serializers import ActivitySerializerGet, ActivitySerializerPut
from users.permissions import IsFollowingOrOwner, IsOwner

class ActivityList(generics.ListCreateAPIView):
    serializer_class = ActivitySerializerGet
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)  

class ActivityListOfUser(generics.ListAPIView):
    serializer_class = ActivitySerializerGet
    permission_classes = [permissions.IsAuthenticated, IsFollowingOrOwner]

    def get_queryset(self):
        return Activity.objects.filter(user__id = self.kwargs['pk'])

class ActivityDetailed(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializerPut
    permission_classes = [permissions.IsAuthenticated, IsOwner] 

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.title = request.data['title']
        instance.description = request.data['description']
        instance.activity_enum_value = request.data['activity_enum_value']
        instance.start_time = request.data['start_time']
        instance.end_time = request.data['end_time']
        if request.data['tag'] == '':
            instance.tag = None
        else:
            instance.tag = request.data['tag']

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"message": "Could not update activity", "details": serializer.errors})
