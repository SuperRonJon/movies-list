from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    tmdb_id = models.IntegerField(unique=True)
    popularity = models.FloatField()
    release_date = models.CharField(max_length=12)
    overview = models.CharField(max_length=1000)

class Tag(models.Model):
    movie = models.ForeignKey(Movie, to_field="tmdb_id",on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
