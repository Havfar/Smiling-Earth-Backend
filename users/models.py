from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_user_id(self):
        return self.pk

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.CharField(max_length=300)

    def get_followers_count(self):
        return Follower.objects.filter(user = self.user).exclude(is_followed_by = self.user).count()

    def get_following_count(self):
        return Follower.objects.filter(is_followed_by = self.user).count()

    def get_email(self):
        return self.user



class Follower(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    is_followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_followed_by')

    def get_user_info(self):
        user_dict = vars(self.user)
        return {"id": user_dict["id"], "email": user_dict["email"]}

    def get_is_followed_by_info(self):
        user_dict = vars(self.is_followed_by)
        return {"id": user_dict["id"], "email": user_dict["email"]}
        
    def get_following(self, user):
        return Follower.objects.filter(is_followed_by=user)

    def get_followers(self, user):
        return Follower.objects.filter(user=user).exclude(is_followed_by=user)

    def get_following_count(self, user):
        return Follower.objects.filter(is_followed_by=user).count()

    def get_followers_count(self, user):
        return Follower.objects.filter(user=user).count()
        
    def __str__(self):
        return str(self)
