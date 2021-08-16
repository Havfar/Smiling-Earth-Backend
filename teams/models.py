from users.models import User
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_admin')
    location = models.CharField(max_length=8)
    is_public = models.BooleanField(default=True)

    def get_members_count(self):
        return Member.objects.filter(team = self.pk).count()

    def get_teams(self):
        return Team.objects.filter(self.is_public)

    def get_teams_by_location(self):
        return Team.objects.filter(location = self.location)

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member_of_team')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team')

    def get_user_info(self):
        user_dict = vars(self.user)
        return {"id": user_dict["id"], "email": user_dict["email"]}

    def get_members_count(self, team):
        return Member.objects.filter(team = team).count()

    def get_user_is_member_of(self):
        return Member.objects.filter(user = self.user)
    
class Rival(models.Model):
    sender = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='receiver')
    
    ACCEPTED = "a"
    PENDING = "p"
    DECLINED = "d"
    STATUS_CHOICES = (
        (ACCEPTED, "Accepted"),
        (PENDING, "Pending"),
        (DECLINED, "Declined"),
    )

    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)

