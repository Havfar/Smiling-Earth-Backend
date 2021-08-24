from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField
from django.contrib.auth import get_user_model
from activities.activities import Activities

class ActivityTag(models.Model):
    title = CharField(max_length=200)

class Activity(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='Activities'
    )
    title = CharField(max_length=200)
    description = TextField(null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    activity_enum_value = models.IntegerField(default=Activities.WALK.value)
    tag = models.ForeignKey(ActivityTag, on_delete=models.SET_NULL, related_name='activity_tag', blank=True, null=True)
