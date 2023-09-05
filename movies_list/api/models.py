from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    tmdb_id = models.IntegerField()
    popularity = models.FloatField()
    release_date = models.CharField(max_length=12)
    overview = models.CharField(max_length=1000)
