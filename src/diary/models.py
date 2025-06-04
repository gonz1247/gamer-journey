from django.db import models

from game.models import Game
from patron.models import Patron

# Create your models here.
class DiaryEntry(models.Model):
    # owner of the diary
    patron = models.ForeignKey(Patron, on_delete=models.CASCADE)
    # games shouldn't be deleted from the DB once added but will protect just in case
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    platform = models.CharField(max_length=100)
    # these will all be optional when setting up the input form
    review = models.TextField()
    rating = models.FloatField(null=True)
    completed_date = models.DateField()
    completion_status = models.BooleanField()
    hours = models.IntegerField(null=True)
    # entry time will be used to better sort when multiple games were finished on the same day
    entry_datetime = models.DateTimeField()