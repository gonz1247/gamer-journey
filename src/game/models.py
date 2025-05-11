from django.db import models

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)

