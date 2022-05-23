from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=100, blank=True)
    gameID = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
