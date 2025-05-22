from django.db import models
from django.contrib.auth.models import User
from game.models import Game
# Create your models here.

# TODO: Give myself (superuser) a patron account manually
class Patron(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wishlist = models.ManyToManyField(Game)
    fav_platform = models.CharField(max_length=25)
