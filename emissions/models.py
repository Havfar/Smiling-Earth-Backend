from django.db import models
from django.db.models.deletion import CASCADE
from users.models import User

# Create your models here.


class Emission(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_emissions')
    # date = models.DateField()
    emissions = models.FloatField()
    isSourceTransport = models.BooleanField()
