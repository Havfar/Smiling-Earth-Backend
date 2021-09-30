from django.db.models import fields
from rest_framework.serializers import ModelSerializer

from emissions.models import Emission


class EmissionSerializer(ModelSerializer):
    class Meta:
        model = Emission
        fields = ['id', 'emissions', 'user_id']
