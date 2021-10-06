from django.db.models import fields
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import Profile
from users.serializers import ProfileSerializer, UserSerializer

from emissions.models import Emission


class EmissionSerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source="get_profile")

    class Meta:
        model = Emission
        fields = ['id', 'emissions', 'user',
                  'isSourceTransport', 'year', 'month', 'weekNo']


class TeamEmissionSerializer(ModelSerializer):

    class Meta:
        model = Emission
        fields = ['id', 'emissions',
                  'isSourceTransport', 'year', 'month', 'weekNo']
