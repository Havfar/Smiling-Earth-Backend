from django.db.models import fields
from rest_framework import serializers
from teams.models import Team, Member

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    members_count = serializers.IntegerField(source = 'get_members_count')
    class Meta:
        model = Team
        fields = ['id','name', 'members_count']

class TeamDetailSerializer(serializers.HyperlinkedModelSerializer):
    # admin = #TODO
    class Meta:
        model = Team
        fields = ['id','name', 'description']
        # fields = ['id','name', 'description', 'admin']
    
class MemberSerializer(serializers.ModelSerializer):
    # member = serializers.DictField(child = serializers.CharField(), source = 'get_user_info', read_only = True)
    user = serializers.DictField(child = serializers.CharField(), source = 'get_user_info', read_only = True)

    # users = []
    class Meta:
        model = Member
        fields = ['user']
        read_only_fields = ['user']
    

    