from django.db import models

class GameCategory(models.Model):
    """Database model for relationship between games and categories"""
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
