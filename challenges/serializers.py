from rest_framework import serializers
from challenges.models import Challenge

class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'start_date', 'end_date']