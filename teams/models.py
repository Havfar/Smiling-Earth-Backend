from django.db import models
from django.db.models.query_utils import Q
from emissions.models import Emission
from emissions.serializers import EmissionSerializer, TeamEmissionSerializer
from users.models import Profile, User
from users.serializers import ProfileSerializer


class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='team_admin')
    location = models.CharField(max_length=8)
    is_public = models.BooleanField(default=True)
    symbol = models.CharField(max_length=20)

    def get_members_count(self):
        return Member.objects.filter(team=self.pk).count()

    def get_teams(self):
        return Team.objects.filter(self.is_public)

    def get_teams_by_location(self):
        return Team.objects.filter(location=self.location)

    def get_team_emission(self):
        emissions = 0.0

        members = Member.objects.filter(team=self.pk)
        for member in members:
            user_emission = Emission.objects.filter(Q(user=member.user))
            for emission in user_emission:
                emissions += emission.emissions

        return emissions

    def get_team_detailed_emission(self):
        emission_transport = 0.0
        emission_energy = 0.0

        members = Member.objects.filter(team=self.pk)
        for member in members:
            user_emission = Emission.objects.filter(Q(user=member.user))
            for emission in user_emission:
                if emission.isSourceTransport:
                    emission_transport += emission.emissions
                else:
                    emission_energy += emission.emissions

        return {"transport": emission_transport, "energy": emission_energy}


class Member(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='member_of_team')
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='team')

    def get_user_info(self):
        user_dict = vars(self.user)
        return {"id": user_dict["id"], "email": user_dict["email"]}

    def get_user_profile(self):
        user = Profile.objects.get(user=self.user)
        serializer = ProfileSerializer(many=False, instance=user)

        return serializer.data

    def get_user_emissions(self):
        emitted = 0.0
        emissions = Emission.objects.filter(user=self.user)
        for emission in emissions:
            emitted += emission.emissions
        # serializer = TeamEmissionSerializer(many=True, instance=emissions)
        return emitted

    def get_members_count(self):
        return Member.objects.filter(team=self.team).count()

    def get_user_is_member_of(self):
        return Member.objects.filter(user=self.user)


class Rival(models.Model):
    sender = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='receiver')

    ACCEPTED = "a"
    PENDING = "p"
    DECLINED = "d"
    STATUS_CHOICES = (
        (ACCEPTED, "Accepted"),
        (PENDING, "Pending"),
        (DECLINED, "Declined"),
    )

    # def get_rival(self):
    #     self.
    #     return self.sender

    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default=PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)
