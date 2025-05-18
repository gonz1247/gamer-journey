from django.db import models

from game.models import Game, Platform


# Create your models here.
class DiaryEntry(models.Model):
    # games and platforms shouldn't be deleted from the DB once added but will protect just in case
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    # these will all be optional when setting up the input form
    review = models.TextField()
    rating = models.IntegerField()
    completed_date = models.DateField()
    completion_status = models.BooleanField()
    hours = models.IntegerField()