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

    def __str__(self):
        return self.name


SCORES = [
    (1, '1 - Trash'),
    (2, '2 - Horrible'),
    (3, '3 - Bad'),
    (4, '4 - Not Good'),
    (5, '5 - OK'),
    (6, '6 - Enjoyable'),
    (7, '7 - Good'),
    (8, '8 - Very Good'),
    (9, '9 - Perfect'),
    (10, '10 - Master Piece'), 
]


class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=80)
    body = models.TextField()
    score = models.PositiveSmallIntegerField(choices=SCORES)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Review {self.body} by {self.name}"
