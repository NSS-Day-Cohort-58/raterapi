from django.db import models
from django.contrib.auth.models import User

class GameRating(models.Model):
    """Database model for a game rating"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_on = models.DateField()
