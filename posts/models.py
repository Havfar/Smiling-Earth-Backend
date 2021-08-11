from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Post(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField()

    class Meta:
        ordering = ['timestamp']


