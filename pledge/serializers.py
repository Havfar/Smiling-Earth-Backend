from activities import serializers
from django.db.models.fields import BooleanField
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

from pledge.models import Pledge, TeamPledge, UserPledge


class PledgeSerializer(ModelSerializer):
    class Meta:
        model = Pledge
        fields = ['id', 'title', 'description', 'color', 'icon']


class UserPledgeSerializer(ModelSerializer):
    pledge = PledgeSerializer(read_only=True)

    class Meta:
        model = UserPledge
        fields = ['pledge']


class TeamPledgeSerializer(ModelSerializer):
    pledge = PledgeSerializer(read_only=True)

    class Meta:
        model = TeamPledge
        fields = ['id', 'pledge', 'team']
