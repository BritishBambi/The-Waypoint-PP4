from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=100, blank=True)
    gameID = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


RATE_CHOICES = [
    (1, '1 - Trash'),
    (2, '2 - Terrible'),
    (3, '3 - Bad'),
    (4, '4 - Not Great'),
    (5, '5 - OK'),
    (6, '6 - Decent'),
    (7, '7 - Good'),
    (8, '8 - Very Good'),
    (9, '9 - Almost Perfect'),
    (10, '10 - Masterpiece'),
]


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=3000, blank=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)

    def __str__(self):
        return self.game.name
