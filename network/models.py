from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content= models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(User, related_name="liked_posts", blank=True)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    follower = models.ManyToManyField(User,  blank=True, related_name="followers")
    following= models.ManyToManyField(User,  blank=True, related_name="following")