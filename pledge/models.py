from django.db import models
from django.contrib.auth import get_user_model

class Pledge(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=100)
    color = models.CharField(max_length=15)

class UserPledge(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='pledge_user')
    pledge = models.ForeignKey(Pledge, on_delete=models.Case, related_name='pledge')