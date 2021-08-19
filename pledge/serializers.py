from django.db.models.base import Model
from pledge.models import Pledge, UserPledge
from rest_framework.serializers import ModelSerializer


class PledgeSerializer(ModelSerializer):
    class Meta:
        model = Pledge
        fields = ['id', 'title', 'description', 'color', 'icon']

class UserPledgeSerializer(ModelSerializer):
    class Meta:
        model = UserPledge
        fields = ['id', 'pledge','user']