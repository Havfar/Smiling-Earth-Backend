from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField
from django.contrib.auth import get_user_model
class Activity(models.Model):
# Create your models here.
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='Activities'
    )
    title = CharField(max_length=200)
    description = TextField()
    start_time = models.DateTimeField()
    timestamp = models.DateTimeField()

    # TODO: Lag Enum
    type = CharField(max_length=200)
    
    