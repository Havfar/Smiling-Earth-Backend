from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .managers import CustomUserManager


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
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, primary_key=True, related_name='profile_user')

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.CharField(max_length=300)

    # fluttermoji
    topType = models.IntegerField(default=0)
    accessoriesType = models.IntegerField(default=0)
    hairColor = models.IntegerField(default=0)
    facialHairType = models.IntegerField(default=0)
    facialHairColor = models.IntegerField(default=0)
    clotheType = models.IntegerField(default=0)
    eyeType = models.IntegerField(default=0)
    eyebrowType = models.IntegerField(default=0)
    mouthType = models.IntegerField(default=0)
    skinColor = models.IntegerField(default=0)
    clotheColor = models.IntegerField(default=0)
    style = models.IntegerField(default=0)
    graphicType = models.IntegerField(default=0)

    def get_followers_count(self):
        return Follower.objects.filter(user=self.user).exclude(is_followed_by=self.user).count()

    def get_following_count(self):
        return Follower.objects.filter(is_followed_by=self.user).count()

    def get_email(self):
        return self.user

    def get_avatar(self):
        return {
            "topType": self.topType,
            "accessoriesType": self.accessoriesType,
            "hairColor": self.hairColor,
            "facialHairType": self.facialHairType,
            "facialHairColor": self.facialHairColor,
            "clotheType": self.clotheType,
            "eyeType": self.eyeType,
            "eyebrowType": self.eyebrowType,
            "mouthType": self.mouthType,
            "skinColor": self.skinColor,
            "clotheColor": self.clotheColor,
            "style": self.style,
            "graphicType": self.graphicType
        }


class Follower(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    is_followed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='is_followed_by')

    def get_profile(self):
        profile = Profile.objects.get(user=self.user)
        serializer = _ProfileSerializer(instance=profile)
        return serializer.data

    def get_followed_by_profile(self):
        profile = Profile.objects.get(user=self.is_followed_by)
        serializer = _ProfileSerializer(instance=profile)
        return serializer.data

    def get_following(self, user):
        return Follower.objects.filter(is_followed_by=user)

    def get_followers(self, user):
        return Follower.objects.filter(user=user).exclude(is_followed_by=user)

    def get_following_count(self, user):
        return Follower.objects.filter(is_followed_by=user).count()

    def get_followers_count(self, user):
        return Follower.objects.filter(user=user).count()

    def is_following(self):
        following = Follower.objects.filter(
            user=self.is_followed_by, is_followed_by=self.user)
        return following.count() > 0
        # return False

    def __str__(self):
        return str(self)


# Private serializer to prevent circular import error
class _ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_id', 'first_name', 'last_name']
