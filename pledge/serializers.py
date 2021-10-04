from activities import serializers
from rest_framework.serializers import ModelSerializer

from pledge.models import Pledge, TeamPledge, UserPledge


class PledgeSerializer(ModelSerializer):
    # icon_utf =
    class Meta:
        model = Pledge
        fields = ['id', 'title', 'description', 'color', 'icon']


class UserPledgeSerializer(ModelSerializer):
    class Meta:
        model = UserPledge
        fields = ['id', 'pledge', 'user']


class TeamPledgeSerializer(ModelSerializer):
    pledge = PledgeSerializer(read_only=True)

    class Meta:
        model = TeamPledge
        fields = ['id', 'pledge', 'team']
