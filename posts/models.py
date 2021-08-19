from django.db import models
from django.contrib.auth import get_user_model

class Post(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="posts"
    )
    content = models.CharField(max_length=300)

    def get_likes_count(self):
        return Like.objects.filter(post = self).count()

    def get_comments_count(self):
        return Comment.objects.filter(post = self).count()
    class Meta:
        ordering = ['timestamp']

class Like(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="likes"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")

class Comment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="comment"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    content = models.CharField(max_length=300)


