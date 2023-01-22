from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, default=None, related_name="liked_posts")

    def serialize(self, user):
        return {
            "id": self.id,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes.count(),
            "liked": self in Profile.objects.filter(user=user).first().liked_posts.all(),
        }

    def __str__(self):
        return str(self.id)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.CharField(
        max_length=255, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')
    about = models.TextField(blank=True)
    followers = models.ManyToManyField(
        User, blank=True, related_name="followers_all")

    def serialize(self, user):
        return {
            "username": self.user.username,
            "profile_img": self.profile_img,
            "about": self.about,
            "followers": self.followers.count(),
            "following": self.user.followers.count(),
            "get_followers": self in Profile.objects.filter(user=user).first().followers_all.all(),
        }

    def __str__(self):
        return str(self.user)
