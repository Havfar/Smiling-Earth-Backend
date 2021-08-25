from rest_framework.serializers import ModelSerializer
from pledge.models import Pledge, UserPledge


class PledgeSerializer(ModelSerializer):
    class Meta:
        model = Pledge
        fields = ['id', 'title', 'description', 'color', 'icon']


class UserPledgeSerializer(ModelSerializer):
    class Meta:
        model = UserPledge
        fields = ['id', 'pledge', 'user']
