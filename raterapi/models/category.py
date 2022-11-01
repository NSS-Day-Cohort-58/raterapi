from django.db import models

class Category(models.Model):
    """Database model for Games"""
    description = models.CharField(max_length=1000)
