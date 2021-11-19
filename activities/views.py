from django.utils.translation import activate
from posts.models import Post
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from users.permissions import IsFollowingOrOwner, IsOwner

from activities.models import Activity
from activities.serializers import ActivitySerializerGet, ActivitySerializerPut


class ActivityList(generics.ListCreateAPIView):
    serializer_class = ActivitySerializerGet
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     challenge = get_object_or_404(Challenge, id=request.data['challenge'])
    #     activity = Activity.objects.create(
    #         user = request.user,
    #         title = request.data['title'],
    #         description = request.data['description'],
    #         start_time = request.data['title'],
    #         title = request.data['title'],
    #     )

    #     if created:
    #         Post.objects.create(
    #             user=request.user, content="Joined the challenge", challenge=challenge)
    #     return Response({"challenge user": {"id": challenge_user.id}}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        if serializer.is_valid():

            activity = serializer.save(user=self.request.user)
            Post.objects.create(
                user=self.request.user, content="Completed an activity!", activity=activity)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Could not update activity", "details": serializer.errors})


class ActivityListOfUser(generics.ListAPIView):
    serializer_class = ActivitySerializerGet
    permission_classes = [permissions.IsAuthenticated, IsFollowingOrOwner]

    def get_queryset(self):
        return Activity.objects.filter(user__id=self.kwargs['pk'])


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

        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response({"message": "Could not update activity", "details": serializer.errors})
