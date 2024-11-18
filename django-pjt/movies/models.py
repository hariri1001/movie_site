from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100) # 영화제목
    overview = models.TextField() # 영화줄거리
    release_date = models.DateField() # 개봉일
    vote_count = models.IntegerField() # 평점 개수
    vote_average = models.FloatField() # 평점 평균
    poster_path = models.CharField(max_length=200) # 영화 포스터
    genre_ids = models.ManyToManyField(Genre) # 장르
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies') # 좋아요한 회원
    
    def __str__(self):
       return self.title


class Rank(models.Model):
    pass