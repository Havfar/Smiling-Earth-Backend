from rest_framework import serializers

from teams.models import Member, Rival, Team


class TeamSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(source='get_members_count')
    emissions = serializers.ReadOnlyField(source='get_team_emission')

    class Meta:
        model = Team
        fields = ['id', 'name', 'members_count', 'symbol', 'emissions']


class TeamDetailSerializer(serializers.ModelSerializer):
    emissions = serializers.ReadOnlyField(source='get_team_detailed_emission')

    class Meta:
        model = Team
        fields = ['id', 'name', 'symbol',
                  'description', 'location', 'emissions']


class MemberSerializer(serializers.ModelSerializer):
    user = serializers.DictField(
        child=serializers.CharField(), source='get_user_info', read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'user']
        read_only_fields = ['id', 'user']


class MemberEmissionsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='get_user_profile')
    # emissions = serializers.DateField(
    #     child=serializers.CharField(), source='get_user_emission', read_only=True)
    emissions = serializers.ReadOnlyField(
        source="get_user_emissions", read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'user', 'emissions']
        ordering = ('emissions',)
        # read_only_fields = ['id', 'user', 'emissions']

# class MemberEmissions


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
    sender = TeamSerializer(read_only=True)
    receiver = TeamSerializer(read_only=True)
    team = TeamSerializer(read_only=True, source='get_rival')

    class Meta:
        model = Rival
        fields = [
            'id',
            'sender',
            'receiver',
            'status',
            'team'
        ]



# class RivalEmissionSerializer(serializers.ModelSerializer):
#     emissions = serializers.ReadOnlyField(source='get_emissions')
#     team1 = serializers.SlugRelatedField(read_only=True, slug_field='name')
#     receiver = TeamSerializer(read_only=True)

#     class Meta:
#         model = Rival
#         fields = [
#             'team1',
#             'receiver',
#             'status'
#         ]


class TeamEmissionSerializer(serializers.ModelSerializer):

    class Meta:
        mode = Member
