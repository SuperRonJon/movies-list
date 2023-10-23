from django.db import models

# Create your models here.
class Collection(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    tmdb_id = models.IntegerField()
    popularity = models.FloatField()
    release_date = models.CharField(max_length=12)
    overview = models.CharField(max_length=1000)
    poster_path = models.CharField(max_length=1000)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)


class Tag(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
