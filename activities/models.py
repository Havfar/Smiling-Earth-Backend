from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField

from activities.activities import Activities


class ActivityTag(models.Model):
    title = TextField(max_length=200)


class Activity(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="Activities"
    )
    title = TextField(max_length=200)
    description = TextField(null=True)
    start_time = DateTimeField()
    end_time = DateTimeField()
    activity_enum_value = models.IntegerField(default=Activities.WALK.value)
    tag = models.ForeignKey(
        ActivityTag,
        on_delete=models.SET_NULL,
        related_name="activity_tag",
        blank=True,
        null=True
    )
