from django.db import models

from game.models import Game, Platform
from patron.models import Patron


# Create your models here.
class DiaryEntry(models.Model):
    # owner of the diary
    patron = models.ForeignKey(Patron, on_delete=models.CASCADE)
    # games and platforms shouldn't be deleted from the DB once added but will protect just in case
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    # these will all be optional when setting up the input form
    review = models.TextField()
    rating = models.FloatField(null=True)
    completed_date = models.DateField()
    completion_status = models.BooleanField()
    hours = models.IntegerField(null=True)