from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationsList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        notifications = Notification.objects.filter(to_user=user)
        return notifications


class NotificationsUpdate(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user_has_seen = True

        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response({"message": "Could not update notification", "details": serializer.errors})
