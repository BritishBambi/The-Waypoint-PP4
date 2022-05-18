from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# Create your models here.


class Game(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(default='game-slug')
    background_image = CloudinaryField('image', default='placeholder')
    background_image_url = models.URLField(blank=True)
    description = models.CharField(max_length=2000, blank=True)
    platforms = models.CharField(max_length=40, blank=True)
    developer = models.CharField(max_length=100, blank=True)
    genres = models.CharField(max_length=100, blank=True)
    release_date = models.DateField(auto_now_add=False)
    reviews = models.ManyToManyField(User, related_name='game_reviews', blank=True)

    def __str__(self):
        return self.name

