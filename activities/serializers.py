from django.db.models import fields
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from activities.models import Activity


class ActivitySerializerGet(ModelSerializer):
    # user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Activity
        fields = [
            "id",
            # "user",
            "title",
            "description",
            "start_time",
            "end_time",
            "tag",
            "activity_enum_value"
        ]


class ActivitySerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = ["title"]


class ActivitySerializerPut(ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            "title",
            "description",
            "start_time",
            "end_time",
            "tag",
            "activity_enum_value"
        ]
