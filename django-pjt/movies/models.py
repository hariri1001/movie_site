from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    release_date = models.DateField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    poster_path = models.CharField(max_length=200)
    genre_ids = models.ManyToManyField(Genre)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    
    def __str__(self):
       return self.title


class Rank(models.Model):
    pass