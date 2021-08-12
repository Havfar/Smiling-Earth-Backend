from django.db.models import fields
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedRelatedField
from activities.models import Activity

class ActivitySerializer(HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.email')
    class Meta:
        model = Activity
        fields = ['id', 'user', 'title', 'description']