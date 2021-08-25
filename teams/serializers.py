from rest_framework import serializers

from teams.models import Member, Rival, Team


class TeamSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(source='get_members_count')

    class Meta:
        model = Team
        fields = ['id', 'name', 'members_count']


class TeamDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'admin', 'location']


class MemberSerializer(serializers.ModelSerializer):
    user = serializers.DictField(
        child=serializers.CharField(), source='get_user_info', read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'user']
        read_only_fields = ['id', 'user']


class JoinTeamSerializer(serializers.ModelSerializer):

    def validate(self, data):
        user = data['user']
        team = data['team']
        already_member = Member.objects.filter(user=user, team=team).first()
        if already_member:
            raise Exception('already a member')
        return data

    class Meta:
        model = Member
        fields = ['user', 'team']


class LeaveTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['user', 'team']


class RivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rival
        fields = [
            'sender',
            'receiver',
            'status'
        ]
