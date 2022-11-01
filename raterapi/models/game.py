from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    """Database model for Games"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=55)
    release_year = models.IntegerField()
    image_file = models.CharField(max_length=255)
    number_of_players = models.IntegerField()
    description = models.CharField(max_length=1000)
    designer = models.CharField(max_length=75)
    time_to_play = models.IntegerField()
    recommended_age = models.IntegerField()
    categories = models.ManyToManyField('Category', through='GameCategory')
