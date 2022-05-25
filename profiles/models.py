from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

from game.models import Game

# Create your models here.

default_img = 'https://res.cloudinary.com/jojocloudci/image/upload/v1653441917/default-profile_fb2lrf.jpg'


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name='profile')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    bio = models.CharField(max_length=700, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    profile_image = CloudinaryField('image', default=default_img)
    to_play = models.ManyToManyField(Game, related_name='to_play')
    played = models.ManyToManyField(Game, related_name='played')

    def __str__(self):
        return str(self.user)
