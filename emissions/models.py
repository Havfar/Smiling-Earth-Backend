from django.db import models
from django.db.models.deletion import CASCADE
from users.models import Profile, User
from users.serializers import ProfileSerializer

# Create your models here.


class Emission(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_emissions')
    year = models.IntegerField(default=2021)
    month = models.IntegerField(default=10)
    weekNo = models.IntegerField(default=40)
    emissions = models.FloatField()
    isSourceTransport = models.BooleanField()

    def get_profile(self):
        profile = Profile.objects.get(user_id=self.user.pk)
        serializer = ProfileSerializer(profile)
        return serializer.data
